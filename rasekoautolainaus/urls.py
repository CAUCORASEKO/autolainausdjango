
#rasekoautolainaus/urls.py

from django.urls import path
from . import views  # Importamos las vistas de la app

urlpatterns = [
    # Página de inicio - login
    path('', views.login_view, name='login'),
    
    # Logout para cerrar sesión
    path('logout/', views.logout_view, name='logout'),
    
    # Hallintapaneeli (requiere autenticación)
    path('hallinto/', views.hallinto_view, name='hallinto'),
    
    # Reitti ajoneuvon lainaamiseen
    path('lainaus/<int:auto_id>/', views.lainaus_view, name='lainaus'),
    
    # Reitti ajoneuvon palautukseen
    path('palautus/<int:lainaus_id>/', views.palautus_view, name='palautus'),
    
    # Manuaalinen paluureitti
    path('palautus/manual/<int:auto_id>/', views.palautus_manual_view, name='palautus_manual'),
]

