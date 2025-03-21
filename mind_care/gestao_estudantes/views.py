import os
from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import ValidationError
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Administrador, Emocoes, Relatorios, Organization, Server, City, Student
from .forms import AddressForm, OrganizationForm, StudentForm, ServerForm
import json
import requests
import logging


class AdministradorListView(ListView):
    model = Administrador
    template_name = 'administrador_list.html'

class AdministradorDetailView(DetailView):
    model = Administrador
    template_name = 'administrador_detail.html'

class AdministradorCreateView(CreateView):
    model = Administrador
    template_name = 'administrador_form.html'
    fields = ['nome', 'contatos', 'email', 'sexo', 'senha']
    success_url = reverse_lazy('administrador-list')

class AdministradorUpdateView(UpdateView):
    model = Administrador
    template_name = 'administrador_form.html'
    fields = ['nome', 'contatos', 'email', 'sexo', 'senha']
    success_url = reverse_lazy('administrador-list')

class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'administrador_confirm_delete.html'
    success_url = reverse_lazy('administrador-list')

class EmocoesListView(ListView):
    model = Emocoes
    template_name = 'emocoes_list.html'

class RelatoriosListView(ListView):
    model = Relatorios
    template_name = 'relatorios_list.html'



# Função para verificar se o usuário é administrador
def is_admin(user):
    return user.is_staff

# Função para verificar se o usuário é servidor
def is_server(user):
    return user.groups.filter(name='Servidor').exists()


#LOGINs

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home_logado')
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            request.session['user_type'] = 'admin' if user.is_staff else 'server'
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home_logado')

        # Autenticação manual para Administrador
        administrador = Administrador.objects.filter(email=email).first()
        if administrador and administrador.senha == senha:
            # Criando e salvando um usuário temporário
            user, created = User.objects.get_or_create(username=administrador.email)
            user.is_staff = True  # Permissão de admin
            user.save()

            login(request, user)  # Login seguro
            request.session['user_id'] = administrador.id_adm
            request.session['user_type'] = 'admin'
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home_logado')

        # Autenticação manual para Servidor
        servidor = Server.objects.filter(email=email).first()
        if servidor and check_password(senha, servidor.password):
            user, created = User.objects.get_or_create(username=servidor.email)
            user.save()

            login(request, user)
            request.session['user_id'] = servidor.id
            request.session['user_type'] = 'server'
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home_logado')

        messages.error(request, "Credenciais inválidas. Tente novamente.")

    return render(request, "login.html", {"user_type": request.session.get("user_type")})

@login_required
def logout_view(request):
    logout(request)
    request.session.flush() 
    return redirect('login')

@login_required
def minha_conta(request):
    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')

    servidor = None
    admin = None

    if user_type == 'server':
        servidor = Server.objects.filter(id=user_id).first()
    elif user_type == 'admin':
        admin = Administrador.objects.filter(id_adm=user_id).first()

    return render(request, 'minha_conta.html', {
        'user': request.user,
        'user_type': user_type,
        'admin': admin,
        'servidor': servidor,
    })

#Proteção view
def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_type' not in request.session:
            return HttpResponseForbidden("Acesso negado")
        return view_func(request, *args, **kwargs)
    return wrapper

def reset_password(request, token):
    server = get_object_or_404(Server, reset_token=token)

    if request.method == "POST":
        new_password = request.POST.get("password")
        server.password = make_password(new_password)  # Salvar a senha hash
        server.reset_token = ""  # Remover o token após o uso
        server.save()
        return redirect('login')
    
    send_mail(
        'Definição de senha',
        f'Olá, {server.name}!\n\nSua senha foi alterada com sucesso.\n\nAtenciosamente, Mind Care Edu.',
        settings.DEFAULT_FROM_EMAIL,
        [server.email],
        fail_silently=False,
    )

    return render(request, "resetar_senha.html", {"server": server})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Verificar o tipo de usuário
        user_type = request.session.get('user_type')

        if user_type == 'admin':
            # Obter o Administrador
            administrador = Administrador.objects.get(id_adm=request.session.get('user_id'))
            if administrador.senha != current_password:
                messages.error(request, 'Senha atual incorreta.')
                return redirect('change_password')
            if new_password != confirm_password:
                messages.error(request, 'As senhas não correspondem.')
                return redirect('change_password')

            # Atualizar a senha
            administrador.senha = new_password
            administrador.save()

            # Enviar e-mail para o administrador
            send_mail(
                'Definição de Senha',
                f'Olá, {administrador.nome}!\n\nSua senha foi criada com sucesso.\n\nAtenciosamente, Mind Care Edu.',
                settings.DEFAULT_FROM_EMAIL,
                [administrador.email],
                fail_silently=False,
            )

            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('home')

        elif user_type == 'server':
            # Obter o Servidor
            servidor = Server.objects.get(id=request.session.get('user_id'))
            if not check_password(current_password, servidor.password):
                messages.error(request, 'Senha atual incorreta.')
                return redirect('change_password')
            if new_password != confirm_password:
                messages.error(request, 'As senhas não correspondem.')
                return redirect('change_password')

            # Atualizar a senha
            servidor.password = make_password(new_password)
            servidor.save()

            # Enviar e-mail para o servidor
            send_mail(
                'Redefinição de Senha',
                f'Olá, {servidor.name}!\n\nSua senha foi alterada com sucesso.\n\nAtenciosamente, Mind Care Edu.',
                settings.DEFAULT_FROM_EMAIL,
                [servidor.email],
                fail_silently=False,
            )

            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('home')

    return render(request, 'change_password.html')

# View para listar as organizações

@login_required
@user_passes_test(is_admin)
def list_organizations(request):
    if request.method == 'POST':
        organization_id = request.POST.get('organization_id')
        organization = get_object_or_404(Organization, id=organization_id)
        organization.delete()
    # Pesquisar por nome se houver parâmetro 'q'
    query = request.GET.get('q', '')
    organizations = Organization.objects.filter(Q(name__icontains=query))

    return render(request, 'list_organizations.html', {'organizations': organizations})

@login_required
@user_passes_test(is_admin)
@csrf_exempt
def create_organization(request):
    cities = City.objects.all()
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        organization_form = OrganizationForm(request.POST)
        
        if address_form.is_valid() and organization_form.is_valid():
            # Salva o endereço
            address = address_form.save()
            organization = organization_form.save(commit=False)
            organization.address = address
            organization.save()

            return redirect('list_organizations')
        else:
            # Exibe erros de formulário para depuração
            print(address_form.errors)
            print(organization_form.errors)
    
    else:
        address_form = AddressForm()
        organization_form = OrganizationForm()

    return render(request, "create_organization.html", {
        "organization_form": organization_form,
        "address_form": address_form,
        "cities": cities
    })

@login_required
@user_required
def student_create(request):
    organizations = Organization.objects.filter(active=True)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        print(request.POST)  # Verifique o conteúdo dos dados enviados
        if form.is_valid():
            form.save()
            return redirect('student_list')
        else:
            print(form.errors)  # Exibe os erros de validação
    else:
        form = StudentForm()
    return render(request, 'student_create.html', {'form': form, 'organizations': organizations})

@login_required
@user_required
def student_list(request):
    # Excluir estudante se o método for POST
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        student.delete()

    # Pesquisar por nome se houver parâmetro 'q'
    query = request.GET.get('q', '')
    students = Student.objects.filter(Q(name__icontains=query))

    return render(request, 'student_list.html', {'students': students})
logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_admin)
def importar_alunos(request):
    organizations = Organization.objects.all()
    
    if request.method == "POST":
        organization_id = request.POST.get('organization_id')
        json_file = request.FILES.get('json_file')
        
        # Validação básica
        if not organization_id or not json_file:
            messages.error(request, "Selecione uma organização e um arquivo JSON válido.")
            return redirect('importar_alunos')
            
        try:
            # Limitar tamanho do arquivo (5MB)
            max_size = 5 * 1024 * 1024
            if json_file.size > max_size:
                messages.error(request, "Arquivo muito grande (máximo 5MB).")
                return redirect('importar_alunos')
                
            # Processar arquivo
            data = json.loads(json_file.read().decode('utf-8'))
            organization = get_object_or_404(Organization, id=organization_id)
            
            resultados = {"novos": 0, "atualizados": 0, "erros": 0}
            
            if isinstance(data, list):
                for index, aluno in enumerate(data, start=1):
                    try:
                        # Validar campos obrigatórios
                        if not all(field in aluno for field in ['matricula', 'nome']):
                            resultados["erros"] += 1
                            logger.warning(f"Registro {index} inválido: campos obrigatórios faltando")
                            continue
                            
                        # Mapear dados
                        student_data = {
                            'code': aluno['matricula'],
                            'name': aluno['nome'],
                            'phone': aluno.get('telefone', ''),
                            'email': aluno.get('email', ''),
                            'gender': aluno.get('genero', 'O').upper()[:1],
                            'organization': organization,
                            'active': True
                        }
                        
                        # Processar foto
                        foto_url = aluno.get('foto')
                        if foto_url:
                            try:
                                response = requests.get(foto_url, timeout=5)
                                if response.status_code == 200:
                                    student_data['photo'] = ContentFile(
                                        response.content, 
                                        name=f"{aluno['matricula']}.jpg"
                                    )
                            except Exception as e:
                                logger.error(f"Erro ao baixar foto: {str(e)}")
                        
                        # Criar/atualizar estudante
                        student, created = Student.objects.update_or_create(
                            code=student_data['code'],
                            defaults=student_data
                        )
                        
                        if created:
                            resultados["novos"] += 1
                        else:
                            resultados["atualizados"] += 1
                            
                    except Exception as e:
                        resultados["erros"] += 1
                        logger.error(f"Erro no registro {index}: {str(e)}")
                        
                # Mensagem final
                msg = (f"Importação concluída! "
                       f"Novos: {resultados['novos']}, "
                       f"Atualizados: {resultados['atualizados']}, "
                       f"Erros: {resultados['erros']}")
                       
                if resultados['erros'] > 0:
                    messages.warning(request, msg)
                else:
                    messages.success(request, msg)
                    
                return redirect('student_list')
                
            else:
                messages.error(request, "Formato JSON inválido: o arquivo deve conter uma lista de alunos.")
                return redirect('importar_alunos')
                
        except json.JSONDecodeError:
            messages.error(request, "Arquivo JSON inválido ou corrompido.")
            logger.error("Falha ao decodificar JSON", exc_info=True)
            return redirect('importar_alunos')
            
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            logger.critical("Erro crítico na importação", exc_info=True)
            return redirect('importar_alunos')
    
    # GET request
    return render(request, "import_alunos.html", {
        "organizations": organizations
    })


@login_required
@user_passes_test(is_admin)
def importar_suap(request):

    user_type = request.session.get('user_type')
    user_id = request.session.get('user_id')
    
    try:

        if user_type == 'server':
            server = Server.objects.get(id=user_id)
            organization = server.organization
        elif user_type == 'admin':
            organization = Organization.objects.first()
        else:
            messages.error(request, "Acesso não autorizado.")
            return redirect('student_list')

        # Configurações da API SUAP
        SUAP_API_URL = getattr(settings, 'SUAP_API_URL', 'https://suap.example.com/api/v2/edu/alunos/')
        SUAP_TOKEN = getattr(settings, 'SUAP_TOKEN', 'seu-token-aqui')

        headers = {
            'Authorization': f'Bearer {SUAP_TOKEN}',
            'Accept': 'application/json'
        }

        alunos = []
        next_page = SUAP_API_URL
        
        while next_page:
            response = requests.get(next_page, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            alunos.extend(data['results'])
            next_page = data['next'] 


        novos = 0
        atualizados = 0

        for aluno_suap in alunos:

            student_data = {
                'code': aluno_suap['matricula'],
                'name': aluno_suap['nome_usual'],
                'email': aluno_suap['email'],
                'gender': aluno_suap['sexo'][0].upper() if aluno_suap['sexo'] else 'O',
                'phone': aluno_suap.get('telefone', ''),
                'organization': organization
            }


            obj, created = Student.objects.update_or_create(
                code=student_data['code'],
                defaults=student_data
            )

            if created:
                novos += 1
            else:
                atualizados += 1

        messages.success(request, f"SUAP: {novos} novos, {atualizados} atualizados")
    
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Erro na conexão com o SUAP: {str(e)}")
    except Exception as e:
        messages.error(request, f"Erro inesperado: {str(e)}")

    return redirect('student_list')

@login_required
@user_passes_test(is_admin)
def create_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        
        if form.is_valid():
            server = form.save(commit=False)
            
            # Gerar um token único para redefinição de senha
            token = get_random_string(32)
            server.reset_token = token  # Campo na model do servidor
            server.save()

            # Criar o link de redefinição de senha
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[token]))

            # Enviar e-mail para o servidor
            send_mail(
                'Defina sua senha',
                f'Olá, {server.name}!\n\nVocê foi cadastrado no sistema. Clique no link abaixo para definir sua senha:\n\n{reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [server.email],
                fail_silently=False,
            )

            return redirect('home')
    
    else:
        form = ServerForm()

    organizations = Organization.objects.all()
    return render(request, 'create_servidor.html', {'form': form, 'organizations': organizations})

@login_required
@user_passes_test(is_admin)
def server_list(request):
    # Excluir estudante se o método for POST
    if request.method == 'POST':
        server_id = request.POST.get('server_id')
        server = get_object_or_404(Server, id=server_id)
        server.delete()

    # Pesquisar por nome se houver parâmetro 'q'
    query = request.GET.get('q', '')
    servers = Server.objects.filter(Q(name__icontains=query))

    return render(request, 'server_list.html', {'servers': servers})



@csrf_exempt
def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        contatos = request.POST.get('contatos')
        email = request.POST.get('email')
        sexo = request.POST.get('sexo')
        senha = request.POST.get('password')

        # Validar campos básicos (adapte conforme necessário)
        if not nome or not email or not senha:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return redirect('cadastro.html')

        # Verifica se o e-mail já está em uso
        if Administrador.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return redirect('cadastro.html')

        # Criar novo administrador
        administrador = Administrador(
            nome=nome,
            contatos=contatos,
            email=email,
            sexo=sexo,
            senha=senha,  #Utilize hashing para senhas
        )
        administrador.save()

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login.html')  # Substitua pelo nome da página de login ou outra página

    return render(request, 'cadastro.html')

@csrf_exempt
def receber_emocoes(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        emocao = Emocoes(
            matricula_id=dados['matricula'],
            descricao=dados['descricao'],
            emocao_detectada=dados['emocao_detectada'],
            data_hora=dados['data_hora'],
            confianca=dados['confianca'],
            foto=dados['foto'],
        )
        emocao.save()
        return JsonResponse({'status': 'Emoção recebida e armazenada com sucesso'})

@csrf_exempt
def receber_relatorios(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        relatorio = Relatorios(
            matricula_id=dados['matricula'],
            id_emocao_id=dados['id_emocao'],
            emocao_detectada=dados['emocao_detectada'],
            relatorio=dados['relatorio'],
            data_hora=dados['data_hora'],
        )
        relatorio.save()
        return JsonResponse({'status': 'Relatório recebido e armazenado com sucesso'})
    
def home(request):
    user_type = request.session.get('user_type')
    return render(request, "home.html", {'user_type': user_type})

@login_required
def home_logado(request):
    user_type = request.session.get('user_type')
    return render(request, "home_logado.html", {'user_type': user_type})