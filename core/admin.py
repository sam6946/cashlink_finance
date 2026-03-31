from django.contrib import admin
from .models import DemandeTransaction


@admin.register(DemandeTransaction)
class DemandeTransactionAdmin(admin.ModelAdmin):
    list_display = ['nom_complet', 'numero_telephone', 'montant', 'statut', 'date_soumission']
    list_filter = ['statut', 'date_soumission']
    search_fields = ['nom_complet', 'numero_telephone']
    readonly_fields = ['code_secret', 'date_soumission']
    list_per_page = 25
