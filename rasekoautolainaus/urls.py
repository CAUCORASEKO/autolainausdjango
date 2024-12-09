from django.urls import path
from . import views

urlpatterns = [
    path('', views.hallinto_view, name='hallinto'),  # Esto hace que la raíz se redirija a la vista hallinto
    path('hallinto/', views.hallinto_view, name='hallinto'),  # Panel de administración
    path('lainaus/<int:auto_id>/', views.lainaus_view, name='lainaus'),  # Ruta para el préstamo de un vehículo
]
