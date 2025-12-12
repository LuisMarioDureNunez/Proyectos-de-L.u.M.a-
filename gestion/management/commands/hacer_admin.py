from django.core.management.base import BaseCommand
from gestion.models import UsuarioPersonalizado

class Command(BaseCommand):
    help = 'Convierte un usuario en administrador'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = UsuarioPersonalizado.objects.get(username=username)
            user.rol = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Usuario {username} ahora es ADMINISTRADOR'))
        except UsuarioPersonalizado.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Usuario {username} no existe'))
