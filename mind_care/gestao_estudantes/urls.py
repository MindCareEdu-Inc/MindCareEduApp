from django.urls import path
from . import views

urlpatterns = [
  
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('estudante/criar/', views.student_create, name='student_create'),
    path('estudantes/', views.student_list, name='student_list'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('receber-emocoes/', views.receber_emocoes, name='receber-emocoes'),
    path('receber-relatorios/', views.receber_relatorios, name='receber-relatorios'),
    path('emocoes/', views.EmocoesListView.as_view(), name='emocoes-list'),
    path('cadastro/', views.cadastro, name='cadastro'),  # Define a rota para o cadastro
    path('relatorios/', views.RelatoriosListView.as_view(), name='relatorios-list'),
]