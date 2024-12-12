from django.urls import path
from . import views

urlpatterns = [
    # Juuri ohjataan hallinto-näkymään
    # Tämä reitti vie hallintapaneeliin, jossa voidaan hallita autoja
    path('', views.hallinto_view, name='hallinto'),  # Juuri ohjataan hallinto-näkymään
    
    # Hallinnon hallintapaneeli
    # Tämä reitti vie käyttäjän autojen hallintanäkymään,
    # jossa voi lisätä ja hallita autoja
    path('hallinto/', views.hallinto_view, name='hallinto'),  # Hallinnon hallintapaneeli
    
    # Reitti ajoneuvon lainaamiseen
    # Tämä reitti vie ajoneuvon lainaussivulle, jossa voidaan tehdä lainaustapahtuma
    path('lainaus/<int:auto_id>/', views.lainaus_view, name='lainaus'),  # Reitti ajoneuvon lainaamiseen
    
    # Reitti ajoneuvon palautukseen
    # Tämä reitti vie käyttäjän palautus-sivulle, jossa voi merkitä auton palautetuksi
    path('palautus/<int:lainaus_id>/', views.palautus_view, name='palautus'),  # Reitti ajoneuvon palautukseen
]
