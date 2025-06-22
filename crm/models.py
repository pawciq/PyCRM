# crm/models.py
from django.db import models
from django.contrib.auth.models import User


# Użyjemy CharField z choices dla statusów, aby łatwo nimi zarządzać
class LeadStatus(models.TextChoices):
    NOWY = 'new', 'Nowy'
    PIERWSZY_KONTAKT = 'first_contact', 'Pierwszy kontakt'
    ZAINTERESOWANY = 'interested', 'Zainteresowany'
    BRAK_ODPOWIEDZI = 'no_answer', 'Brak odpowiedzi'
    BRAK_KONKRETOW = 'no_details', 'Brak konkretów'
    STRACONY = 'lost', 'Stracony'


class LeadSource(models.TextChoices):
    FACEBOOK = 'fb', 'Facebook'
    TELEGRAM = 'tg', 'Telegram'
    INSTAGRAM = 'ig', 'Instagram'
    OGLOSZENIE = 'ad', 'Ogłoszenie'
    INNE = 'other', 'Inne'


class Lead(models.Model):
    """ Model reprezentujący potencjalnego klienta (Leada). """
    nazwa = models.CharField(max_length=255, verbose_name="Nazwa (np. imię i nazwisko)")
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NOWY, verbose_name="Status")
    zrodlo = models.CharField(max_length=20, choices=LeadSource.choices, verbose_name="Źródło")
    komentarz = models.TextField(blank=True, verbose_name="Komentarz")
    menedzer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="leady",
                                 verbose_name="Menedżer")

    # Biuro/oddział - na razie jako pole tekstowe
    biuro = models.CharField(max_length=100, blank=True, verbose_name="Biuro")

    utworzono = models.DateTimeField(auto_now_add=True)
    zaktualizowano = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leady"
        ordering = ['-utworzono']

    def __str__(self):
        return self.nazwa


class Klient(models.Model):
    """ Model reprezentujący klienta, który powstał z leada. """
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, verbose_name="Powiązany lead")
    imie_nazwisko = models.CharField(max_length=255, verbose_name="Imię i nazwisko")
    telefon = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    pesel = models.CharField(max_length=11, blank=True, verbose_name="PESEL")
    menedzer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="klienci",
                                 verbose_name="Menedżer")

    utworzono = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"

    def __str__(self):
        return self.imie_nazwisko


class Zadanie(models.Model):
    """ Model dla zadań do zrobienia. """
    # Używamy GenericForeignKey, aby zadanie mogło być powiązane z dowolnym modelem (np. Leadem, Klientem)
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType

    tytul = models.CharField(max_length=255, verbose_name="Tytuł/Opis zadania")
    termin = models.DateTimeField(verbose_name="Termin wykonania")
    wykonane = models.BooleanField(default=False, verbose_name="Czy wykonane?")
    przypisane_do = models.ForeignKey(User, on_delete=models.CASCADE, related_name="zadania",
                                      verbose_name="Przypisane do")

    # Pola dla GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    utworzono = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"
        ordering = ['termin']

    def __str__(self):
        return self.tytul