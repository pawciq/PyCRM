# crm/urls.py
from django.urls import path
# TO JEST OSTATECZNA, POPRAWNA LINIA IMPORTU - ZAWIERA WSZYSTKIE 5 WIDOKÓW
from .views import (
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView
)

app_name = 'crm'

urlpatterns = [
    # Każda ścieżka ma teraz swój zaimportowany widok
    path('', LeadListView.as_view(), name='lead-list'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('lead/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('lead/<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('lead/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
]