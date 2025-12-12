#!/usr/bin/env python3
"""
Generador de iconos PWA para Mi Tienda Premium
Crea iconos en diferentes tamaños para PWA
"""

import os
from PIL import Image, ImageDraw, ImageFont
import sys

def crear_icono_pwa(size, output_path):
    """Crear un icono PWA con el logo de la empresa"""
    
    # Crear imagen con fondo degradado
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fondo con gradiente azul
    for y in range(size):
        # Gradiente de azul a naranja
        r = int(102 + (255 - 102) * y / size)  # 102 -> 255
        g = int(126 + (102 - 126) * y / size)  # 126 -> 102  
        b = int(234 + (0 - 234) * y / size)    # 234 -> 0
        
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Agregar círculo central
    margin = size // 8
    circle_size = size - (margin * 2)
    circle_pos = (margin, margin, margin + circle_size, margin + circle_size)
    
    # Círculo blanco con transparencia
    draw.ellipse(circle_pos, fill=(255, 255, 255, 200), outline=(255, 255, 255, 255), width=3)
    
    # Texto "MT" (Mi Tienda)
    try:
        # Intentar usar una fuente del sistema
        font_size = size // 4
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Usar fuente por defecto si no encuentra arial
        font = ImageFont.load_default()
    
    # Texto principal
    text = "MT"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - size // 20
    
    # Sombra del texto
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 100), font=font)
    # Texto principal
    draw.text((text_x, text_y), text, fill=(0, 35, 149, 255), font=font)
    
    # Texto pequeño debajo
    try:
        small_font_size = size // 12
        small_font = ImageFont.truetype("arial.ttf", small_font_size)
    except:
        small_font = ImageFont.load_default()
    
    small_text = "Premium"
    small_bbox = draw.textbbox((0, 0), small_text, font=small_font)
    small_text_width = small_bbox[2] - small_bbox[0]
    
    small_x = (size - small_text_width) // 2
    small_y = text_y + text_height + size // 20
    
    draw.text((small_x, small_y), small_text, fill=(255, 102, 0, 255), font=small_font)
    
    # Guardar imagen
    img.save(output_path, 'PNG', optimize=True)
    print(f"✅ Icono creado: {output_path} ({size}x{size})")

def main():
    """Función principal"""
    
    # Directorio de iconos
    icons_dir = "static/icons"
    
    # Crear directorio si no existe
    os.makedirs(icons_dir, exist_ok=True)
    
    # Tamaños de iconos PWA estándar
    sizes = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]
    
    print("🎨 Generando iconos PWA para Mi Tienda Premium...")
    print("=" * 50)
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f"icon-{size}x{size}.png")
        try:
            crear_icono_pwa(size, output_path)
        except Exception as e:
            print(f"❌ Error creando icono {size}x{size}: {e}")
    
    # Crear favicon.ico
    try:
        favicon_path = "static/favicon.ico"
        crear_icono_pwa(32, "temp_favicon.png")
        
        # Convertir a ICO
        img = Image.open("temp_favicon.png")
        img.save(favicon_path, format='ICO', sizes=[(32, 32)])
        
        # Limpiar archivo temporal
        os.remove("temp_favicon.png")
        print(f"✅ Favicon creado: {favicon_path}")
        
    except Exception as e:
        print(f"❌ Error creando favicon: {e}")
    
    print("=" * 50)
    print("🎉 ¡Iconos PWA generados exitosamente!")
    print("\nIconos creados:")
    
    for size in sizes:
        icon_path = os.path.join(icons_dir, f"icon-{size}x{size}.png")
        if os.path.exists(icon_path):
            file_size = os.path.getsize(icon_path)
            print(f"  📱 {icon_path} - {file_size} bytes")
    
    print(f"\n📋 Total de iconos: {len([s for s in sizes if os.path.exists(os.path.join(icons_dir, f'icon-{s}x{s}.png'))])}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Proceso cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)