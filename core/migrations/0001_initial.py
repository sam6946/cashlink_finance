from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='DemandeTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_complet', models.CharField(max_length=200, verbose_name='Nom complet')),
                ('numero_telephone', models.CharField(max_length=20, verbose_name='Numéro de téléphone')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant à recevoir (FCFA)')),
                ('code_secret', models.CharField(max_length=128, verbose_name='Code secret')),
                ('statut', models.CharField(
                    choices=[
                        ('en_attente', 'En attente'),
                        ('en_traitement', 'En traitement'),
                        ('complete', 'Complété'),
                        ('rejete', 'Rejeté'),
                    ],
                    default='en_attente',
                    max_length=20,
                    verbose_name='Statut',
                )),
                ('date_soumission', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de soumission')),
                ('date_traitement', models.DateTimeField(blank=True, null=True, verbose_name='Date de traitement')),
                ('notes_admin', models.TextField(blank=True, verbose_name='Notes administrateur')),
            ],
            options={
                'verbose_name': 'Demande de transaction',
                'verbose_name_plural': 'Demandes de transactions',
                'ordering': ['-date_soumission'],
            },
        ),
    ]
