import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('bio', models.TextField(blank=True, default='')),
                ('date_naissance', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=500)),
                ('sous_titre', models.CharField(blank=True, default='', max_length=500)),
                ('couverture', models.URLField(blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('isbn', models.CharField(blank=True, default='', max_length=20)),
                ('themes', models.JSONField(blank=True, default=dict)),
                ('auteurs', models.ManyToManyField(blank=True, related_name='livres', to='books.auteur')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.PositiveSmallIntegerField()),
                ('commentaire', models.TextField(blank=True, default='')),
                ('utilisateur', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='evaluations',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('livre', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='evaluations',
                    to='books.livre',
                )),
            ],
            options={
                'unique_together': {('utilisateur', 'livre')},
            },
        ),
        migrations.CreateModel(
            name='UserLivre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utilisateur', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user_livres',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('livre', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user_livres',
                    to='books.livre',
                )),
            ],
            options={
                'unique_together': {('utilisateur', 'livre')},
            },
        ),
    ]
