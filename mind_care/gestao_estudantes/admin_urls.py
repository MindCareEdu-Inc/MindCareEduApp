from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('receber-relatorios/', views.receber_relatorios, name='receber-relatorios'),
    path('estudantes/', views.student_list, name='student_list'),
    path('importar-suap/', views.importar_suap, name='importar_suap'),
    path('importar-alunos/', views.importar_alunos, name='importar_alunos'),
    path('organizações/', views.list_organizations, name='list_organizations'),
    path('organizações/criar/', views.create_organization, name='create_organization'),
    path('servidor/criar/', views.create_server, name='server_create'),
    path('servidores/', views.server_list, name='server_list'),
]
