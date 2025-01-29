from django.urls import path
from . import views

urlpatterns = [
  
    path('', views.home, name='home'),
    path('home1/', views.home1, name='home1'),
    path('student/create/', views.student_create, name='student_create'),
    path('organizations/', views.list_organizations, name='list_organizations'),
    path('organizations/create/', views.create_organization, name='create_organization'),
    path('server/create/', views.create_server, name='server_create'),
    path('receber-emocoes/', views.receber_emocoes, name='receber-emocoes'),
    path('receber-relatorios/', views.receber_relatorios, name='receber-relatorios'),
    path('emocoes/', views.EmocoesListView.as_view(), name='emocoes-list'),
    path('cadastro/', views.cadastro, name='cadastro'),  # Define a rota para o cadastro
    path('relatorios/', views.RelatoriosListView.as_view(), name='relatorios-list'),
    path('administradores/', views.AdministradorListView.as_view(), name='administrador-list'),
    path('administradores/novo/', views.AdministradorCreateView.as_view(), name='administrador-create'),
    path('administradores/<int:pk>/', views.AdministradorDetailView.as_view(), name='administrador-detail'),
    path('administradores/<int:pk>/editar/', views.AdministradorUpdateView.as_view(), name='administrador-update'),
    path('administradores/<int:pk>/deletar/', views.AdministradorDeleteView.as_view(), name='administrador-delete'),
]
