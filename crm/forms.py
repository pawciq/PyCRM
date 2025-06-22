# crm/forms.py
from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'nazwa',
            'status',
            'zrodlo',
            'menedzer',
            'biuro',
            'komentarz',
        ]

        # Możemy też dodać widgety, aby formularz wyglądał lepiej, np. dla komentarza
        widgets = {
            'komentarz': forms.Textarea(attrs={'rows': 3}),
        }