from django.core.management.base import BaseCommand
from gestion.notifications import NotificationSystem

class Command(BaseCommand):
    help = 'Revisa productos con stock bajo y envía notificaciones'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostrar información detallada',
        )
    
    def handle(self, *args, **options):
        verbose = options['verbose']
        
        if verbose:
            self.stdout.write('🔍 Revisando productos con stock bajo...')
        
        cantidad_notificaciones = NotificationSystem.check_low_stock_and_notify()
        
        if verbose:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Se enviaron {cantidad_notificaciones} notificaciones de stock bajo'
                )
            )