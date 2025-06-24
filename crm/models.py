# crm/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# --- Modele dla Leadów i Zadań (bez zmian) ---

class LeadStatus(models.TextChoices):
    NOWY = 'new', 'Nowy'
    PIERWSZY_KONTAKT = 'first_contact', 'Pierwszy kontakt'
    ZAINTERESOWANY = 'interested', 'Zainteresowany'
    BRAK_ODPOWIEDZI = 'no_answer', 'Brak odpowiedzi'
    BRAK_KONKRETOW = 'no_details', 'Brak konkretów'
    STRACONY = 'lost', 'Stracony'
    SKONWERTOWANY = 'converted', 'Skonwertowany'


class LeadSource(models.TextChoices):
    FACEBOOK = 'fb', 'Facebook'
    TELEGRAM = 'tg', 'Telegram'
    INSTAGRAM = 'ig', 'Instagram'
    OGLOSZENIE = 'ad', 'Ogłoszenie'
    INNE = 'other', 'Inne'


class Lead(models.Model):
    nazwa = models.CharField(max_length=255, verbose_name="Nazwa (np. imię i nazwisko)")
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NOWY, verbose_name="Status")
    zrodlo = models.CharField(max_length=20, choices=LeadSource.choices, verbose_name="Źródło")
    komentarz = models.TextField(blank=True, verbose_name="Komentarz")
    menedzer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="leady",
                                 verbose_name="Menedżer")
    biuro = models.CharField(max_length=100, blank=True, verbose_name="Biuro")
    utworzono = models.DateTimeField(auto_now_add=True)
    zaktualizowano = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leady"
        ordering = ['-utworzono']

    def __str__(self):
        return self.nazwa


class Zadanie(models.Model):
    tytul = models.CharField(max_length=255, verbose_name="Tytuł/Opis zadania")
    termin = models.DateTimeField(verbose_name="Termin wykonania")
    wykonane = models.BooleanField(default=False, verbose_name="Czy wykonane?")
    przypisane_do = models.ForeignKey(User, on_delete=models.CASCADE, related_name="zadania",
                                      verbose_name="Przypisane do")
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


# --- NOWE I ZAKTUALIZOWANE MODELE ---

class Klient(models.Model):
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


class Zamowienie(models.Model):
    class Status(models.TextChoices):
        OCZEKUJE_NA_PLATNOSC = 'pending_payment', 'Oczekuje na płatność'
        W_REALIZACJI = 'processing', 'W realizacji'
        ZAKONCZONE = 'completed', 'Zakończone'
        ANULOWANE = 'canceled', 'Anulowane'
        PROBLEM = 'problem', 'Problem'
        ZWROT_KAUCJI = 'deposit_return', 'Zwrot kaucji'

    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='zamowienia', verbose_name="Klient")
    menedzer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Menedżer")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OCZEKUJE_NA_PLATNOSC,
                              verbose_name="Status")

    ma_rachunek = models.BooleanField(default=False, verbose_name="Ma rachunek")
    ma_umowe = models.BooleanField(default=False, verbose_name="Ma umowę")

    utworzono = models.DateTimeField(auto_now_add=True)
    zaktualizowano = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"
        ordering = ['-utworzono']

    def __str__(self):
        return f"Zamówienie nr {self.pk} dla {self.klient.imie_nazwisko}"


class Samochod(models.Model):
    class Status(models.TextChoices):
        NA_AUKCJI = 'on_auction', 'Samochód na aukcji'
        W_DRODZE = 'in_transit', 'Samochód w drodze do portu'
        W_PORCIE = 'at_port', 'Samochód w porcie'
        DOSTARCZONY = 'delivered', 'Dostarczony do klienta'

    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.CASCADE, related_name='samochody',
                                   verbose_name="Zamówienie")
    nazwa = models.CharField(max_length=255, verbose_name="Nazwa (np. Ford Edge 2018)")
    vin = models.CharField(max_length=17, unique=True, verbose_name="VIN")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NA_AUKCJI, verbose_name="Status")

    aukcja_info = models.CharField(max_length=255, blank=True, verbose_name="Aukcja / Konto / Lot")
    oplacone_na_aukcji = models.BooleanField(default=False, verbose_name="Opłacone na aukcji")

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"

    def __str__(self):
        return self.nazwa