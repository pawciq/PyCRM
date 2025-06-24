# crm/urls.py
from django.urls import path
from .views import (
    DashboardView,
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView,
    ZadanieCreateView,
    KlientListView,
    KlientDetailView,
    convert_lead_to_klient,
    ZamowienieCreateView,
    ZamowienieDetailView,
    SamochodCreateView  # NOWY IMPORT
)

app_name = 'crm'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    # Ścieżki dla Leadów
    path('leady/', LeadListView.as_view(), name='lead-list'),
    path('lead/create/', LeadCreateView.as_view(), name='lead-create'),
    path('lead/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('lead/<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('lead/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('lead/<int:pk>/convert/', convert_lead_to_klient, name='lead-convert'),
    path('lead/<int:lead_pk>/add-task/', ZadanieCreateView.as_view(), name='zadanie-create'),

    # Ścieżki dla Klientów
    path('klienci/', KlientListView.as_view(), name='klient-list'),
    path('klient/<int:pk>/', KlientDetailView.as_view(), name='klient-detail'),

    # Ścieżki dla Zamówień
    path('klient/<int:klient_pk>/add-order/', ZamowienieCreateView.as_view(), name='zamowienie-create'),
    path('zamowienie/<int:pk>/', ZamowienieDetailView.as_view(), name='zamowienie-detail'),

    # NOWA ŚCIEŻKA DLA TWORZENIA SAMOCHODU
    path('zamowienie/<int:zamowienie_pk>/add-car/', SamochodCreateView.as_view(), name='samochod-create'),
]