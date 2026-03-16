from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count
from .models import Auteur, Livre, UserLivre
from .serializers import (
    AuteurDetailSerializer,
    LivreSerializer,
    EvaluationCreateSerializer,
    UserLivreSerializer,
)


class LivreListView(generics.ListAPIView):
    serializer_class = LivreSerializer

    def get_queryset(self):
        return (
            Livre.objects
            .prefetch_related('auteurs')
            .annotate(
                avg_note=Avg('evaluations__note'),
                count_evaluations=Count('evaluations'),
            )
        )


class EvaluationCreateView(APIView):
    def post(self, request, pk):
        try:
            livre = Livre.objects.get(pk=pk)
        except Livre.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EvaluationCreateSerializer(
            data=request.data,
            context={'livre': livre},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)


class AuteurDetailView(generics.RetrieveAPIView):
    queryset = Auteur.objects.all()
    serializer_class = AuteurDetailSerializer


class UserLivreListView(generics.ListAPIView):
    serializer_class = UserLivreSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return (
            UserLivre.objects
            .filter(utilisateur_id=user_id)
            .select_related('utilisateur', 'livre')
            .prefetch_related('livre__auteurs')
        )
