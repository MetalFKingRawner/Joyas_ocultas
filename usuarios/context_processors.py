from .models import PerfilUsuario


def perfil_usuario(request):
    if request.user.is_authenticated:
        perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
        return {'perfil_usuario': perfil}
    return {}