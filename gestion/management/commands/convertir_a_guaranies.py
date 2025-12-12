from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from gestion.models import Material, Producto, ItemPresupuesto, Presupuesto, Maquinaria, ContratoContratista

class Command(BaseCommand):
    help = 'Convierte todos los precios de dólares a guaraníes paraguayos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tasa-cambio',
            type=float,
            default=7300.0,
            help='Tasa de cambio USD a PYG (default: 7300)'
        )
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirma la conversión sin preguntar'
        )

    def handle(self, *args, **options):
        tasa_cambio = Decimal(str(options['tasa_cambio']))
        
        self.stdout.write(
            self.style.SUCCESS('🇵🇾 CONVERSIÓN DE PRECIOS A GUARANÍES PARAGUAYOS')
        )
        self.stdout.write('=' * 60)
        self.stdout.write(f'💱 Tasa de cambio: 1 USD = {tasa_cambio:,.0f} PYG')
        
        if not options['confirmar']:
            respuesta = input('\n¿Deseas continuar con la conversión? (s/n): ')
            if respuesta.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                self.stdout.write(self.style.WARNING('❌ Conversión cancelada'))
                return

        try:
            with transaction.atomic():
                # Convertir materiales
                materiales = Material.objects.all()
                for material in materiales:
                    precio_original = material.precio
                    material.precio = precio_original * tasa_cambio
                    material.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Materiales convertidos: {materiales.count()}')
                )

                # Convertir productos
                productos = Producto.objects.all()
                for producto in productos:
                    precio_original = producto.precio
                    producto.precio = precio_original * tasa_cambio
                    producto.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Productos convertidos: {productos.count()}')
                )

                # Convertir maquinaria
                maquinarias = Maquinaria.objects.all()
                for maquinaria in maquinarias:
                    if maquinaria.costo_alquiler_dia > 0:
                        maquinaria.costo_alquiler_dia *= tasa_cambio
                        maquinaria.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Maquinarias convertidas: {maquinarias.count()}')
                )

                # Convertir items de presupuesto
                items = ItemPresupuesto.objects.all()
                for item in items:
                    item.precio_unitario *= tasa_cambio
                    item.save()
                
                # Recalcular presupuestos
                presupuestos = Presupuesto.objects.all()
                for presupuesto in presupuestos:
                    presupuesto.calcular_totales()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Items de presupuesto convertidos: {items.count()}')
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Presupuestos recalculados: {presupuestos.count()}')
                )

                # Convertir contratos
                contratos = ContratoContratista.objects.all()
                for contrato in contratos:
                    contrato.monto_total *= tasa_cambio
                    if contrato.anticipo_monto > 0:
                        contrato.anticipo_monto *= tasa_cambio
                    contrato.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Contratos convertidos: {contratos.count()}')
                )

                self.stdout.write('=' * 60)
                self.stdout.write(
                    self.style.SUCCESS('🎉 CONVERSIÓN COMPLETADA EXITOSAMENTE')
                )
                self.stdout.write(
                    self.style.WARNING('💡 Recuerda actualizar tus templates para mostrar "Gs." en lugar de "$"')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante la conversión: {e}')
            )
            raise