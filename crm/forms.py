# crm/forms.py
from django import forms
from django.contrib.auth.models import User
# Dodajemy Samochod do importu
from .models import Lead, Klient, Zadanie, Zamowienie, Samochod


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
        widgets = {
            'komentarz': forms.Textarea(attrs={'rows': 3}),
        }


class ZadanieForm(forms.ModelForm):
    przypisane_do = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Przypisane do",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Zadanie
        fields = [
            'tytul',
            'termin',
            'przypisane_do',
        ]
        widgets = {
            'termin': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'tytul': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class ZamowienieForm(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = [
            'status',
            'ma_rachunek',
            'ma_umowe',
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'ma_rachunek': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ma_umowe': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# NOWY FORMULARZ DLA SAMOCHODÓW
class SamochodForm(forms.ModelForm):
    class Meta:
        model = Samochod
        # Pole 'zamowienie' ustawimy automatycznie w widoku
        fields = [
            'nazwa',
            'vin',
            'status',
            'aukcja_info',
            'oplacone_na_aukcji'
        ]
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'aukcja_info': forms.TextInput(attrs={'class': 'form-control'}),
            'oplacone_na_aukcji': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }