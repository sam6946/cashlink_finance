from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
import hashlib

from .models import DemandeTransaction
from .forms import DemandeTransactionForm


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


def home(request):
    return render(request, 'core/home.html')


def soumettre(request):
    if request.method == 'POST':
        form = DemandeTransactionForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            # Hash the secret code before saving
            raw_code = form.cleaned_data['code_secret']
            # demande.code_secret = hashlib.sha256(raw_code.encode()).hexdigest()
            demande.save()
            return render(request, 'core/confirmation.html', {'demande': demande})
    else:
        form = DemandeTransactionForm()
    return render(request, 'core/formulaire.html', {'form': form})


def confirmation(request):
    return render(request, 'core/confirmation.html')


# ─── Dashboard superuser ───────────────────────────────────────────

def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants incorrects ou accès non autorisé.')
    return render(request, 'core/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


@login_required
@superuser_required
def dashboard(request):
    demandes = DemandeTransaction.objects.all()

    # Filtres
    statut_filtre = request.GET.get('statut', '')
    search = request.GET.get('search', '')

    if statut_filtre:
        demandes = demandes.filter(statut=statut_filtre)
    if search:
        demandes = demandes.filter(nom_complet__icontains=search) | \
                   demandes.filter(numero_telephone__icontains=search)

    # Stats
    total = DemandeTransaction.objects.count()
    en_attente = DemandeTransaction.objects.filter(statut='en_attente').count()
    en_traitement = DemandeTransaction.objects.filter(statut='en_traitement').count()
    complete = DemandeTransaction.objects.filter(statut='complete').count()
    montant_total = DemandeTransaction.objects.filter(statut='complete').aggregate(
        total=Sum('montant'))['total'] or 0

    # Dernières 7 jours
    sept_jours = timezone.now() - timedelta(days=7)
    recentes = DemandeTransaction.objects.filter(date_soumission__gte=sept_jours).count()

    context = {
        'demandes': demandes,
        'total': total,
        'en_attente': en_attente,
        'en_traitement': en_traitement,
        'complete': complete,
        'montant_total': montant_total,
        'recentes': recentes,
        'statut_filtre': statut_filtre,
        'search': search,
        'statut_choices': DemandeTransaction.STATUT_CHOICES,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
@superuser_required
def changer_statut(request, pk):
    if request.method == 'POST':
        try:
            demande = DemandeTransaction.objects.get(pk=pk)
            nouveau_statut = request.POST.get('statut')
            if nouveau_statut in dict(DemandeTransaction.STATUT_CHOICES):
                demande.statut = nouveau_statut
                if nouveau_statut in ('complete', 'rejete'):
                    demande.date_traitement = timezone.now()
                demande.notes_admin = request.POST.get('notes', demande.notes_admin)
                demande.save()
                messages.success(request, f"Statut mis à jour : {demande.get_statut_display()}")
        except DemandeTransaction.DoesNotExist:
            messages.error(request, "Demande introuvable.")
    return redirect('dashboard')
