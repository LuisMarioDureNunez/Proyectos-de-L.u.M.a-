from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q, Count, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import json

from ..models import (
    UsuarioPersonalizado, Obra, Presupuesto, ItemPresupuesto,
    Material, Maquinaria, Herramienta, Notificacion
)
from .serializers import (
    UserLoginSerializer, UserSerializer, MaterialSerializer,
    ObraSerializer, PresupuestoSerializer, NotificacionSerializer,
    DashboardStatsSerializer, PresupuestoCreateSerializer,
    ItemPresupuestoCreateSerializer
)
from ..notifications.manager import NotificationManager

class LoginAPIView(APIView):
    """API View para login de usuarios"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = UserSerializer(user).data
            
            return Response({
                'token': token.key,
                'user': user_data,
                'message': 'Login exitoso'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    """API View para logout de usuarios"""
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    """API View para perfil de usuario"""
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaterialViewSet(viewsets.ModelViewSet):
    """ViewSet para materiales"""
    serializer_class = MaterialSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        queryset = Material.objects.all().order_by('-fecha_creacion')
        
        # Filtrar por búsqueda
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        
        # Filtrar por stock bajo
        stock_bajo = self.request.query_params.get('stock_bajo', None)
        if stock_bajo:
            queryset = queryset.filter(stock__lt=10)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        """Endpoint para materiales con stock bajo"""
        materiales = self.get_queryset().filter(stock__lt=10)
        serializer = self.get_serializer(materiales, many=True)
        return Response(serializer.data)

class ObraViewSet(viewsets.ModelViewSet):
    """ViewSet para obras"""
    serializer_class = ObraSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.es_administrador or user.es_constructor:
            queryset = Obra.objects.all()
        else:
            queryset = Obra.objects.filter(cliente=user)
        
        # Filtrar por estado
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtrar por búsqueda
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(ubicacion__icontains=search)
            )
        
        return queryset.order_by('-fecha_creacion')
    
    @action(detail=True, methods=['get'])
    def presupuestos(self, request, pk=None):
        """Obtener presupuestos de una obra"""
        obra = self.get_object()
        presupuestos = obra.presupuestos.all().order_by('-fecha_creacion')
        serializer = PresupuestoSerializer(presupuestos, many=True)
        return Response(serializer.data)

class PresupuestoViewSet(viewsets.ModelViewSet):
    """ViewSet para presupuestos"""
    serializer_class = PresupuestoSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.es_administrador or user.es_constructor:
            queryset = Presupuesto.objects.all()
        else:
            queryset = Presupuesto.objects.filter(cliente=user)
        
        # Filtrar por estado
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtrar por obra
        obra_id = self.request.query_params.get('obra_id', None)
        if obra_id:
            queryset = queryset.filter(obra_id=obra_id)
        
        return queryset.order_by('-fecha_creacion')
    
    def create(self, request):
        """Crear un nuevo presupuesto con items"""
        try:
            # Crear presupuesto
            presupuesto_serializer = PresupuestoCreateSerializer(data=request.data)
            if not presupuesto_serializer.is_valid():
                return Response(presupuesto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            presupuesto = presupuesto_serializer.save(
                cliente=request.user,
                estado='solicitado'
            )
            
            # Crear items si se proporcionan
            items_data = request.data.get('items', [])
            for item_data in items_data:
                item_serializer = ItemPresupuestoCreateSerializer(data=item_data)
                if item_serializer.is_valid():
                    item_serializer.save(presupuesto=presupuesto)
            
            # Calcular totales
            presupuesto.calcular_totales()
            
            # Enviar notificación
            #NotificationManager.notificar_presupuesto_creado(presupuesto)#
            
            # Retornar presupuesto creado
            serializer = self.get_serializer(presupuesto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def aceptar(self, request, pk=None):
        """Aceptar un presupuesto"""
        presupuesto = self.get_object()
        
        if presupuesto.cliente != request.user:
            return Response(
                {'error': 'Solo el cliente puede aceptar este presupuesto'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not presupuesto.puede_ser_aceptado():
            return Response(
                {'error': 'El presupuesto no puede ser aceptado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        presupuesto.estado = 'aceptado'
        presupuesto.save()
        
        # Enviar notificación
        #NotificationManager.notificar_presupuesto_aceptado(presupuesto)#
        
        serializer = self.get_serializer(presupuesto)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        """Rechazar un presupuesto"""
        presupuesto = self.get_object()
        
        if presupuesto.cliente != request.user:
            return Response(
                {'error': 'Solo el cliente puede rechazar este presupuesto'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        presupuesto.estado = 'rechazado'
        presupuesto.save()
        
        serializer = self.get_serializer(presupuesto)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def generar_pdf(self, request, pk=None):
        """Generar PDF del presupuesto"""
        from ..utils.pdf_utils import PDFGenerator
        
        presupuesto = self.get_object()
        pdf_generator = PDFGenerator()
        pdf_buffer = pdf_generator.generar_pdf_presupuesto(presupuesto)
        
        response = Response(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="presupuesto_{presupuesto.codigo_presupuesto}.pdf"'
        return response

class NotificacionViewSet(viewsets.ModelViewSet):
    """ViewSet para notificaciones"""
    serializer_class = NotificacionSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')
    
    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        """Obtener notificaciones no leídas"""
        notificaciones = self.get_queryset().filter(leida=False)[:20]
        serializer = self.get_serializer(notificaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """Marcar notificación como leída"""
        notificacion = self.get_object()
        notificacion.marcar_como_leida()
        serializer = self.get_serializer(notificacion)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def marcar_todas_leidas(self, request):
        """Marcar todas las notificaciones como leídas"""
        #NotificationManager.marcar_todas_como_leidas(request.user)#
        return Response({'message': 'Todas las notificaciones marcadas como leídas'})

class DashboardAPIView(APIView):
    """API View para datos del dashboard"""
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        user = request.user
        hace_30_dias = timezone.now() - timedelta(days=30)
        
        # Estadísticas básicas
        if user.es_administrador or user.es_constructor:
            total_obras = Obra.objects.count()
            total_presupuestos = Presupuesto.objects.count()
            presupuestos_aceptados = Presupuesto.objects.filter(estado='aceptado').count()
            presupuestos_rechazados = Presupuesto.objects.filter(estado='rechazado').count()
            total_materiales = Material.objects.count()
            obras_en_proceso = Obra.objects.filter(estado='en_proceso').count()
            obras_finalizadas = Obra.objects.filter(estado='finalizada').count()
            
            monto_total_presupuestado = Presupuesto.objects.aggregate(
                total=Sum('total')
            )['total'] or 0
            
            monto_total_aceptado = Presupuesto.objects.filter(estado='aceptado').aggregate(
                total=Sum('total')
            )['total'] or 0
            
        else:
            total_obras = Obra.objects.filter(cliente=user).count()
            total_presupuestos = Presupuesto.objects.filter(cliente=user).count()
            presupuestos_aceptados = Presupuesto.objects.filter(cliente=user, estado='aceptado').count()
            presupuestos_rechazados = Presupuesto.objects.filter(cliente=user, estado='rechazado').count()
            total_materiales = Material.objects.count()  # Los clientes pueden ver todos los materiales
            obras_en_proceso = Obra.objects.filter(cliente=user, estado='en_proceso').count()
            obras_finalizadas = Obra.objects.filter(cliente=user, estado='finalizada').count()
            
            monto_total_presupuestado = Presupuesto.objects.filter(cliente=user).aggregate(
                total=Sum('total')
            )['total'] or 0
            
            monto_total_aceptado = Presupuesto.objects.filter(cliente=user, estado='aceptado').aggregate(
                total=Sum('total')
            )['total'] or 0
        
        stats = {
            'total_obras': total_obras,
            'total_presupuestos': total_presupuestos,
            'presupuestos_aceptados': presupuestos_aceptados,
            'presupuestos_rechazados': presupuestos_rechazados,
            'total_materiales': total_materiales,
            'monto_total_presupuestado': monto_total_presupuestado,
            'monto_total_aceptado': monto_total_aceptado,
            'obras_en_proceso': obras_en_proceso,
            'obras_finalizadas': obras_finalizadas,
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

class PresupuestoRapidoAPIView(APIView):
    """API View para creación rápida de presupuestos"""
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        try:
            data = request.data
            
            # Validar datos requeridos
            obra_id = data.get('obra_id')
            items = data.get('items', [])
            
            if not obra_id or not items:
                return Response(
                    {'error': 'Se requiere obra_id y al menos un item'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Obtener obra
            obra = get_object_or_404(Obra, id=obra_id)
            
            # Verificar permisos
            if not (request.user.es_administrador or obra.cliente == request.user):
                return Response(
                    {'error': 'No tienes permisos para crear presupuestos para esta obra'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Crear presupuesto
            presupuesto = Presupuesto.objects.create(
                obra=obra,
                cliente=request.user,
                descripcion_servicios=data.get('descripcion', 'Presupuesto rápido desde móvil'),
                iva_porcentaje=data.get('iva_porcentaje', 10),
                dias_validez=data.get('dias_validez', 30),
                estado='solicitado'
            )
            
            # Crear items
            for item_data in items:
                ItemPresupuesto.objects.create(
                    presupuesto=presupuesto,
                    tipo=item_data.get('tipo', 'material'),
                    descripcion=item_data.get('descripcion', 'Item rápido'),
                    cantidad=item_data.get('cantidad', 1),
                    unidad_medida=item_data.get('unidad_medida', 'unidad'),
                    precio_unitario=item_data.get('precio_unitario', 0),
                )
            
            # Calcular totales
            presupuesto.calcular_totales()
            
            # Enviar notificación
            NotificationManager.notificar_presupuesto_creado(presupuesto)
            
            serializer = PresupuestoSerializer(presupuesto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
