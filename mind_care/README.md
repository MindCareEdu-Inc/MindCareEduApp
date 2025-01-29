# MindCare - Monitoramento de Saúde Mental Estudantil

## Descrição do Projeto

O **MindCare** é uma plataforma projetada para monitorar a saúde mental de estudantes do ensino médio e universitário, utilizando tecnologias de reconhecimento facial e inteligência artificial. Com base em expressões faciais, histórico acadêmico, notas e presenças, a plataforma gera relatórios personalizados que ajudam profissionais escolares e responsáveis a tomarem decisões informadas e proativas sobre o bem-estar emocional dos alunos.

## Motivação

A saúde mental de estudantes tem enfrentado desafios significativos nos últimos anos, devido a fatores como pressão acadêmica, bullying, e mudanças na fase da vida. Este projeto busca intervir precocemente, proporcionando suporte preventivo e eficaz.

## Funcionalidades

- **Reconhecimento Facial**: Análise das expressões faciais para identificar padrões emocionais.
- **Integração com Dados Acadêmicos**: Uso de histórico de notas, presenças e relatórios de desempenho.
- **Relatórios Personalizados**: Geração de relatórios detalhados para acompanhamento individual.
- **Intervenção Proativa**: Alertas para profissionais escolares e responsáveis sobre possíveis problemas.

## Configuração do Ambiente

### Pré-requisitos

- Python 3.8+
- pip
- Virtualenv (recomendado)

### Instalação

1. Clone o repositório:
	```
	git clone https://github.com/MindCareEdu-Inc/MindCareEduApp.git
 	cd MindCareEduApp
	cd mind-care
	```

2. Crie e ative um ambiente virtual:
	```
	python -m venv venv
	source venv/bin/activate  # Linux/MacOS
	venv\Scripts\activate     # Windows
	```

3. Instale as dependências:
	```
	pip install -r requirements.txt
	```

4. Realize as migrações do banco de dados:
	```
	python manage.py migrate
	```

5. Inicie o servidor:
	```
	python manage.py runserver
	```

6. A aplicação estará disponível em: http://127.0.0.1:8000/
   
