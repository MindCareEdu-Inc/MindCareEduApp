from django.urls import path
from . import views

urlpatterns = [
  
    path('', views.home, name='home'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/create/', views.student_create, name='student_create'),
    path('students/', views.student_list, name='student_list'),
    path('importar-suap/', views.importar_suap, name='importar_suap'),
    path('importar-alunos/', views.importar_alunos, name='importar_alunos'),
    path('organizations/', views.list_organizations, name='list_organizations'),
    path('organizations/create/', views.create_organization, name='create_organization'),
    path('server/create/', views.create_server, name='server_create'),
    path('servers/', views.server_list, name='server_list'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
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