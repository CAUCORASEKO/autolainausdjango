from django.urls import path
from . import views

urlpatterns = [
    path('', views.hallinto_view, name='hallinto'),  # Juuri ohjataan hallinto-näkymään
    path('hallinto/', views.hallinto_view, name='hallinto'),  # Hallinnon hallintapaneeli
    path('lainaus/<int:auto_id>/', views.lainaus_view, name='lainaus'),  # Reitti ajoneuvon lainaamiseen
]
