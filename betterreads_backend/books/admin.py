from django.contrib import admin
from .models import Auteur, Livre, Evaluation, UserLivre


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'date_naissance')
    search_fields = ('nom',)


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'isbn')
    search_fields = ('titre', 'isbn')
    filter_horizontal = ('auteurs',)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'livre', 'note')
    list_filter = ('note',)


@admin.register(UserLivre)
class UserLivreAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'livre')
