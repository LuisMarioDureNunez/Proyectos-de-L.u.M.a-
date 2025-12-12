from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class PDFGenerator:
    """Generador básico de PDFs sin dependencias externas"""
    
    def generar_pdf_presupuesto(self, presupuesto):
        """Generar PDF básico para presupuesto"""
        try:
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=A4)
            
            # Encabezado
            p.drawString(100, 800, f"PRESUPUESTO: {presupuesto.codigo_presupuesto}")
            p.drawString(100, 780, f"OBRA: {presupuesto.obra.nombre}")
            p.drawString(100, 760, f"CLIENTE: {presupuesto.cliente.get_full_name()}")
            
            # Items básicos
            y = 700
            for item in presupuesto.items.all()[:10]:  # Limitar a 10 items
                p.drawString(100, y, f"- {item.descripcion}: {item.cantidad} x Gs. {item.precio_unitario}")
                y -= 20
                if y < 100:  # Evitar salirse de la página
                    break
            
            # Total
            p.drawString(100, y-20, f"TOTAL: Gs. {presupuesto.total:,.0f}")
            
            p.showPage()
            p.save()
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            # Fallback ultra básico
            return self._generar_pdf_fallback(presupuesto)
    
    def _generar_pdf_fallback(self, presupuesto):
        """PDF de fallback ultra simple"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.drawString(100, 750, f"Presupuesto: {presupuesto.codigo_presupuesto}")
        p.drawString(100, 730, f"Obra: {presupuesto.obra.nombre}")
        p.drawString(100, 710, f"Total: Gs. {presupuesto.total:,.0f}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer

class ChartGenerator:
    """Generador de gráficos placeholder - sin dependencias externas"""
    
    def generar_grafico_avance(self, obra):
        """Placeholder para gráfico de avance"""
        return None
    
    def generar_grafico_financiero(self, presupuesto):
        """Placeholder para gráfico financiero"""
        return None
    
    def generar_grafico_stock(self, materiales):
        """Placeholder para gráfico de stock"""
        return None
