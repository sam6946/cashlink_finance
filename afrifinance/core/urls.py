from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('soumettre/', views.soumettre, name='soumettre'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/statut/<int:pk>/', views.changer_statut, name='changer_statut'),
]
