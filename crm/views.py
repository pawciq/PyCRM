# crm/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q  # NOWY, WAŻNY IMPORT

from .models import Lead, Klient, Zadanie, LeadStatus, Zamowienie, Samochod
from .forms import LeadForm, ZadanieForm, ZamowienieForm, SamochodForm


# --- Dashboard ---
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now()
        tasks = Zadanie.objects.filter(przypisane_do=user, wykonane=False)
        context['zalegle_zadania'] = tasks.filter(termin__lt=today.date()).order_by('termin')
        context['dzisiejsze_zadania'] = tasks.filter(termin__date=today.date()).order_by('termin')
        context['jutrzejsze_zadania'] = tasks.filter(termin__date=today.date() + timedelta(days=1)).order_by('termin')
        context['pozniejsze_zadania'] = tasks.filter(termin__date__gt=today.date() + timedelta(days=1)).order_by(
            'termin')
        return context


# --- Widoki dla modelu Lead ---

# MODYFIKUJEMY TEN WIDOK:
class LeadListView(LoginRequiredMixin, ListView):
    # Nie używamy już `model = Lead`, bo queryset budujemy sami
    template_name = 'crm/lead_list.html'
    context_object_name = 'leady'
    # Domyślnie na stronie pokazujemy 15 leadów, aby nie ładować wszystkich naraz
    paginate_by = 15

    def get_queryset(self):
        # Zaczynamy od wszystkich leadów
        queryset = Lead.objects.all().order_by('-utworzono')

        # Pobieramy parametry z adresu URL (np. ?q=szukana_fraza)
        search_query = self.request.GET.get('q', None)
        status_query = self.request.GET.get('status', None)

        # Jeśli użytkownik coś wpisał w pole wyszukiwania
        if search_query:
            # Filtrujemy queryset, szukając frazy w nazwie LUB w komentarzu
            # Q object jest potrzebny do budowania zapytań z warunkiem OR
            # `icontains` oznacza "zawiera, ignorując wielkość liter"
            queryset = queryset.filter(
                Q(nazwa__icontains=search_query) |
                Q(komentarz__icontains=search_query)
            )

        # Jeśli użytkownik wybrał jakiś status z listy
        if status_query and status_query != '':
            queryset = queryset.filter(status=status_query)

        return queryset

    def get_context_data(self, **kwargs):
        # Ta metoda służy do przekazywania dodatkowych danych do szablonu
        context = super().get_context_data(**kwargs)
        # Przekazujemy listę statusów, aby zbudować z nich listę rozwijaną w HTML
        context['status_choices'] = LeadStatus.choices
        # Przekazujemy też aktualnie wybrane wartości, aby formularz je "pamiętał"
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'
    success_url = reverse_lazy('crm:lead-list')

    def form_valid(self, form):
        form.instance.menedzer = self.request.user
        return super().form_valid(form)


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = self.get_object()
        context['zadania'] = Zadanie.objects.filter(content_type__model='lead', object_id=lead.pk)
        return context


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'

    def get_success_url(self):
        return reverse_lazy('crm:lead-detail', kwargs={'pk': self.object.pk})


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    template_name = 'crm/lead_confirm_delete.html'
    success_url = reverse_lazy('crm:lead-list')


# ... reszta widoków bez zmian ...
# --- Widok dla modelu Zadanie ---
class ZadanieCreateView(LoginRequiredMixin, CreateView):
    model = Zadanie
    form_class = ZadanieForm
    template_name = 'crm/zadanie_form.html'

    def form_valid(self, form):
        parent_object = get_object_or_404(Lead, pk=self.kwargs['lead_pk'])
        zadanie = form.save(commit=False)
        zadanie.content_object = parent_object
        if not form.cleaned_data.get('przypisane_do'):
            zadanie.przypisane_do = self.request.user
        zadanie.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('crm:lead-detail', kwargs={'pk': self.kwargs['lead_pk']})


# --- Widoki dla Klientów i Zamówień ---
@require_POST
def convert_lead_to_klient(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if not hasattr(lead, 'klient'):
        klient = Klient.objects.create(lead=lead, imie_nazwisko=lead.nazwa, menedzer=lead.menedzer)
        lead.status = LeadStatus.SKONWERTOWANY
        lead.save()
    return redirect('crm:klient-detail', pk=lead.klient.pk)


class KlientListView(LoginRequiredMixin, ListView):
    model = Klient
    template_name = 'crm/klient_list.html'
    context_object_name = 'klienci'


class KlientDetailView(LoginRequiredMixin, DetailView):
    model = Klient
    template_name = 'crm/klient_detail.html'
    context_object_name = 'klient'


class ZamowienieCreateView(LoginRequiredMixin, CreateView):
    model = Zamowienie
    form_class = ZamowienieForm
    template_name = 'crm/zamowienie_form.html'

    def form_valid(self, form):
        klient = get_object_or_404(Klient, pk=self.kwargs['klient_pk'])
        zamowienie = form.save(commit=False)
        zamowienie.klient = klient
        zamowienie.menedzer = self.request.user
        zamowienie.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('crm:klient-detail', kwargs={'pk': self.kwargs['klient_pk']})


class ZamowienieDetailView(LoginRequiredMixin, DetailView):
    model = Zamowienie
    template_name = 'crm/zamowienie_detail.html'
    context_object_name = 'zamowienie'


class SamochodCreateView(LoginRequiredMixin, CreateView):
    model = Samochod
    form_class = SamochodForm
    template_name = 'crm/samochod_form.html'

    def form_valid(self, form):
        zamowienie = get_object_or_404(Zamowienie, pk=self.kwargs['zamowienie_pk'])
        samochod = form.save(commit=False)
        samochod.zamowienie = zamowienie
        samochod.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('crm:zamowienie-detail', kwargs={'pk': self.kwargs['zamowienie_pk']})