#!/usr/bin/env python3
"""
Generador simple de iconos PWA
"""

import os
from PIL import Image, ImageDraw

def crear_icono_simple(size, output_path):
    """Crear un icono PWA simple"""
    
    # Crear imagen con fondo azul
    img = Image.new('RGB', (size, size), (102, 126, 234))
    draw = ImageDraw.Draw(img)
    
    # Agregar círculo blanco
    margin = size // 6
    circle_size = size - (margin * 2)
    circle_pos = (margin, margin, margin + circle_size, margin + circle_size)
    
    draw.ellipse(circle_pos, fill=(255, 255, 255), outline=(255, 102, 0), width=max(1, size//32))
    
    # Agregar texto "MT"
    text_size = size // 3
    text_x = size // 2 - text_size // 2
    text_y = size // 2 - text_size // 2
    
    # Dibujar "M"
    draw.rectangle([text_x, text_y, text_x + text_size//3, text_y + text_size], fill=(102, 126, 234))
    draw.rectangle([text_x + text_size//3 + text_size//6, text_y, text_x + text_size//3 + text_size//6 + text_size//3, text_y + text_size], fill=(102, 126, 234))
    draw.rectangle([text_x, text_y, text_x + text_size, text_y + text_size//4], fill=(102, 126, 234))
    
    # Guardar imagen
    img.save(output_path, 'PNG')
    print(f"Icono creado: {output_path} ({size}x{size})")

def main():
    """Función principal"""
    
    # Directorio de iconos
    icons_dir = "static/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # Tamaños de iconos PWA
    sizes = [16, 32, 72, 96, 128, 144, 152, 192, 384, 512]
    
    print("Generando iconos PWA...")
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f"icon-{size}x{size}.png")
        try:
            crear_icono_simple(size, output_path)
        except Exception as e:
            print(f"Error creando icono {size}x{size}: {e}")
    
    # Crear favicon
    try:
        favicon_path = "static/favicon.ico"
        crear_icono_simple(32, "temp_favicon.png")
        
        img = Image.open("temp_favicon.png")
        img.save(favicon_path, format='ICO', sizes=[(32, 32)])
        os.remove("temp_favicon.png")
        print(f"Favicon creado: {favicon_path}")
        
    except Exception as e:
        print(f"Error creando favicon: {e}")
    
    print("Iconos PWA generados!")

if __name__ == "__main__":
    main()