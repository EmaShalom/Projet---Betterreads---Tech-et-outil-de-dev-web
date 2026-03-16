from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Auteur, Livre, Evaluation, UserLivre


class AuteurBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = ('id', 'nom')


class AuteurDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = ('id', 'nom', 'bio', 'date_naissance')


class LivreSerializer(serializers.ModelSerializer):
    auteurs = AuteurBriefSerializer(many=True, read_only=True)
    evaluation_moyenne = serializers.SerializerMethodField()
    nombre_evaluations = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = (
            'id', 'titre', 'sous_titre', 'couverture',
            'auteurs', 'description', 'isbn', 'themes',
            'evaluation_moyenne', 'nombre_evaluations',
        )

    def get_evaluation_moyenne(self, obj):
        if hasattr(obj, 'avg_note'):
            return obj.avg_note
        return obj.evaluations.aggregate(avg=Avg('note'))['avg']

    def get_nombre_evaluations(self, obj):
        if hasattr(obj, 'count_evaluations'):
            return obj.count_evaluations
        return obj.evaluations.aggregate(count=Count('id'))['count']


class EvaluationCreateSerializer(serializers.Serializer):
    utilisateur_id = serializers.IntegerField()
    evaluation = serializers.IntegerField(min_value=1, max_value=5)
    commentaire = serializers.CharField(required=False, allow_blank=True, default='')

    def create(self, validated_data):
        livre = self.context['livre']
        obj, _ = Evaluation.objects.update_or_create(
            utilisateur_id=validated_data['utilisateur_id'],
            livre=livre,
            defaults={
                'note': validated_data['evaluation'],
                'commentaire': validated_data.get('commentaire', ''),
            },
        )
        return obj


class UserLivreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='livre.id')
    titre = serializers.CharField(source='livre.titre')
    sous_titre = serializers.CharField(source='livre.sous_titre')
    couverture = serializers.CharField(source='livre.couverture')
    description = serializers.CharField(source='livre.description')
    isbn = serializers.CharField(source='livre.isbn')
    themes = serializers.JSONField(source='livre.themes')
    auteurs = AuteurBriefSerializer(source='livre.auteurs', many=True, read_only=True)
    evaluation = serializers.SerializerMethodField()

    class Meta:
        model = UserLivre
        fields = (
            'id', 'titre', 'sous_titre', 'couverture',
            'description', 'isbn', 'themes', 'auteurs', 'evaluation',
        )

    def get_evaluation(self, obj):
        try:
            ev = Evaluation.objects.get(
                utilisateur=obj.utilisateur,
                livre=obj.livre,
            )
            return ev.note
        except Evaluation.DoesNotExist:
            return None
