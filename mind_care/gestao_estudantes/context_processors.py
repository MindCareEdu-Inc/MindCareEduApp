from django.contrib.auth.models import User
from .models import Administrador, Server  # Ajuste para seu modelo real

def user_info(request):
    if request.user.is_authenticated:

        user_type = request.session.get('user_type')
        user_id = request.session.get('user_id')

        servidor = None
        admin = None

        if user_type == 'server':
            servidor = Server.objects.filter(id=user_id).first()
        elif user_type == 'admin':
            admin = Administrador.objects.filter(id_adm=user_id).first()
        return {
            "user_type": user_type,
            "admin": admin,
            "servidor": servidor,
        }
    
    return {}