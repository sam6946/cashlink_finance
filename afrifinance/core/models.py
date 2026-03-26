from django.db import models
from django.utils import timezone


class DemandeTransaction(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_traitement', 'En traitement'),
        ('complete', 'Complété'),
        ('rejete', 'Rejeté'),
    ]

    nom_complet = models.CharField(max_length=200, verbose_name="Nom complet")
    numero_telephone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant à recevoir (FCFA)")
    code_secret = models.CharField(max_length=128, verbose_name="Code secret")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    date_soumission = models.DateTimeField(default=timezone.now, verbose_name="Date de soumission")
    date_traitement = models.DateTimeField(null=True, blank=True, verbose_name="Date de traitement")
    notes_admin = models.TextField(blank=True, verbose_name="Notes administrateur")

    class Meta:
        verbose_name = "Demande de transaction"
        verbose_name_plural = "Demandes de transactions"
        ordering = ['-date_soumission']

    def __str__(self):
        return f"{self.nom_complet} — {self.montant} FCFA ({self.get_statut_display()})"

    def montant_formate(self):
        return f"{self.montant:,.0f}".replace(',', ' ')
