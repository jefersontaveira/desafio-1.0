from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registrar/', views.registrar_progresso, name='registrar'),
    path('editar/<int:id>/', views.editar_registro, name='editar_registro'),

    path('login/', auth_views.LoginView.as_view(template_name='desafio/login.html'), name='login'),
    # Nova rota de Logout (Sair)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]