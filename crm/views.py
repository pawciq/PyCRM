from django.urls import reverse_lazy
# OTO OSTATECZNA, POPRAWNA LINIA IMPORTU WIDOKÓW
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Lead, Zadanie
from .forms import LeadForm


class LeadListView(ListView):
    model = Lead
    template_name = 'crm/lead_list.html'
    context_object_name = 'leady'


class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'
    success_url = reverse_lazy('crm:lead-list')


class LeadDetailView(DetailView):
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = self.get_object()
        context['zadania'] = Zadanie.objects.filter(
            content_type__model='lead',
            object_id=lead.pk
        )
        return context


class LeadUpdateView(UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'

    def get_success_url(self):
        return reverse_lazy('crm:lead-detail', kwargs={'pk': self.object.pk})


class LeadDeleteView(DeleteView):
    model = Lead
    template_name = 'crm/lead_confirm_delete.html'
    success_url = reverse_lazy('crm:lead-list')