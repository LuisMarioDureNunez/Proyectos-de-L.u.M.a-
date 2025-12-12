"""
GENERADOR DE PDFs PROFESIONALES - LUMA PARAGUAY
Exportación de reportes y presupuestos en PDF
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime

class PDFGenerator:
    """Generador de PDFs profesionales"""
    
    @staticmethod
    def generar_presupuesto(presupuesto):
        """Genera PDF de presupuesto"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        elements.append(Paragraph('🇵🇾 PRESUPUESTO - LUMA PARAGUAY', title_style))
        elements.append(Spacer(1, 20))
        
        # Información del presupuesto
        info_data = [
            ['Código:', presupuesto.codigo_presupuesto],
            ['Fecha:', presupuesto.fecha_creacion.strftime('%d/%m/%Y')],
            ['Cliente:', presupuesto.cliente.get_full_name() or presupuesto.cliente.username],
            ['Obra:', presupuesto.obra.nombre],
            ['Estado:', presupuesto.get_estado_display()]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 30))
        
        # Items del presupuesto
        elements.append(Paragraph('DETALLE DE ITEMS', styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        items_data = [['#', 'Descripción', 'Cant.', 'Precio Unit.', 'Total']]
        for i, item in enumerate(presupuesto.items.all(), 1):
            items_data.append([
                str(i),
                item.descripcion,
                f"{item.cantidad} {item.unidad_medida}",
                f"₲ {item.precio_unitario:,.0f}",
                f"₲ {item.total:,.0f}"
            ])
        
        items_table = Table(items_data, colWidths=[0.5*inch, 3*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 30))
        
        # Totales
        totales_data = [
            ['Subtotal:', f"₲ {presupuesto.subtotal:,.0f}"],
            [f'IVA ({presupuesto.iva_porcentaje}%):', f"₲ {presupuesto.iva_monto:,.0f}"],
            ['TOTAL:', f"₲ {presupuesto.total:,.0f}"]
        ]
        
        totales_table = Table(totales_data, colWidths=[4*inch, 2*inch])
        totales_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#28a745')),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#28a745'))
        ]))
        elements.append(totales_table)
        
        # Pie de página
        elements.append(Spacer(1, 50))
        footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph('LUMA Paraguay - Sistema de Gestión de Obras Civiles', footer_style))
        elements.append(Paragraph(f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}', footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def exportar_presupuesto_pdf(presupuesto):
        """Exporta presupuesto como respuesta HTTP"""
        pdf_buffer = PDFGenerator.generar_presupuesto(presupuesto)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Presupuesto_{presupuesto.codigo_presupuesto}.pdf"'
        
        return response
    
    @staticmethod
    def generar_reporte_obras(obras):
        """Genera PDF de reporte de obras"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#667eea'), alignment=TA_CENTER)
        elements.append(Paragraph('📊 REPORTE DE OBRAS', title_style))
        elements.append(Spacer(1, 20))
        
        data = [['Obra', 'Cliente', 'Estado', 'Presupuesto', 'Fecha Inicio']]
        for obra in obras:
            data.append([
                obra.nombre[:30],
                obra.cliente.username,
                obra.get_estado_display(),
                f"₲ {obra.presupuesto_asignado:,.0f}",
                obra.fecha_inicio.strftime('%d/%m/%Y')
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
