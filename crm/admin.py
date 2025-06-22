# crm/admin.py
from django.contrib import admin
from .models import Lead, Klient, Zadanie

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'status', 'zrodlo', 'menedzer', 'utworzono')
    list_filter = ('status', 'zrodlo', 'menedzer')
    search_fields = ('nazwa', 'komentarz')

@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ('imie_nazwisko', 'telefon', 'menedzer', 'utworzono')
    search_fields = ('imie_nazwisko', 'telefon', 'pesel')

@admin.register(Zadanie)
class ZadanieAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'termin', 'przypisane_do', 'wykonane', 'content_object')
    list_filter = ('wykonane', 'termin', 'przypisane_do')