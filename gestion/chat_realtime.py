"""
SISTEMA DE CHAT EN TIEMPO REAL - LUMA PARAGUAY
Chat entre usuarios con WebSockets
"""
from django.db import models
from django.utils import timezone
from .models import UsuarioPersonalizado

class Conversacion(models.Model):
    """Conversación entre usuarios"""
    participantes = models.ManyToManyField(UsuarioPersonalizado, related_name='conversaciones')
    nombre = models.CharField(max_length=200, blank=True)
    es_grupal = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-actualizado_en']
    
    def __str__(self):
        if self.nombre:
            return self.nombre
        return f"Chat {self.id}"
    
    def ultimo_mensaje(self):
        return self.mensajes.last()

class Mensaje(models.Model):
    """Mensaje en una conversación"""
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='mensajes_enviados')
    contenido = models.TextField()
    archivo = models.FileField(upload_to='chat_archivos/', blank=True, null=True)
    imagen = models.ImageField(upload_to='chat_imagenes/', blank=True, null=True)
    leido = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['creado_en']
    
    def __str__(self):
        return f"{self.remitente.username}: {self.contenido[:50]}"

class MensajeLeido(models.Model):
    """Registro de mensajes leídos por usuario"""
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    leido_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['mensaje', 'usuario']
