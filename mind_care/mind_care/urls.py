"""
URL configuration for mind_care project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from gestao_estudantes import views as gestao_views  # Importe a view home

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('admin/', include('gestao_estudantes.admin_urls')),  # acessa diretamente
    path('gestao/', include('gestao_estudantes.urls')),  # Servidores acessam via /gestao/
    path('minha-conta/', gestao_views.minha_conta, name='minha_conta'),
    path('login/', gestao_views.login_view, name='login'),
    path('home/', gestao_views.home_logado, name='home_logado'),
    path('', gestao_views.home, name='home'),
]

