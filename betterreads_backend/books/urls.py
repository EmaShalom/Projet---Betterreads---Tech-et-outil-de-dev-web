from django.urls import path
from .views import (
    LivreListView,
    EvaluationCreateView,
    AuteurDetailView,
    UserLivreListView,
)

urlpatterns = [
    path('livres/', LivreListView.as_view(), name='livre-list'),
    path('livres/<int:pk>/evaluations/', EvaluationCreateView.as_view(), name='evaluation-create'),
    path('auteurs/<int:pk>/', AuteurDetailView.as_view(), name='auteur-detail'),
    path('users/<int:pk>/livres/', UserLivreListView.as_view(), name='user-livre-list'),
]
