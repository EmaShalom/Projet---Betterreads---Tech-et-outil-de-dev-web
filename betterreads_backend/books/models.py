from django.db import models
from django.conf import settings


class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    bio = models.TextField(blank=True, default='')
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    titre = models.CharField(max_length=500)
    sous_titre = models.CharField(max_length=500, blank=True, default='')
    couverture = models.URLField(blank=True, default='')
    auteurs = models.ManyToManyField(Auteur, related_name='livres', blank=True)
    description = models.TextField(blank=True, default='')
    isbn = models.CharField(max_length=20, blank=True, default='')
    themes = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.titre


class Evaluation(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='evaluations',
    )
    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name='evaluations',
    )
    note = models.PositiveSmallIntegerField()
    commentaire = models.TextField(blank=True, default='')

    class Meta:
        unique_together = ('utilisateur', 'livre')

    def __str__(self):
        return f'{self.utilisateur} — {self.livre} ({self.note})'


class UserLivre(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_livres',
    )
    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE,
        related_name='user_livres',
    )

    class Meta:
        unique_together = ('utilisateur', 'livre')

    def __str__(self):
        return f'{self.utilisateur} — {self.livre}'
