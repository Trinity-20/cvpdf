from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from textwrap import wrap
import json

def cargar_datos_json(ruta_json):
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def agregar_pie_pagina(c):
    ancho, _ = A4
    c.setFont('Helvetica-Oblique', 9)
    c.drawString(50, 20, "ESCUELA DE POSTGRADO DE LA UNAP")
    pie_pagina = f'Página {c.getPageNumber()}'
    c.drawRightString(ancho - 50, 20, pie_pagina)

def agregar_texto(c, texto, x, y, font="Helvetica", size=12, negrita=False, centrado=False):
    c.setFont("Helvetica-Bold" if negrita else font, size)
    if centrado:
        ancho_pagina, _ = A4
        x = (ancho_pagina - c.stringWidth(texto, "Helvetica-Bold" if negrita else font, size)) / 2
    c.drawString(x, y, texto)

def agregar_texto_largo(c, texto, x, y, ancho_maximo, font_name="Helvetica", font_size=12, line_spacing=15):
    c.setFont(font_name, font_size)
    max_chars = int(ancho_maximo / (font_size * 0.5))
    lineas = wrap(texto, width=max_chars)
    for linea in lineas:
        if y < 50:
            c.showPage()
            y = A4[1] - 50
            c.setFont(font_name, font_size)
        c.drawString(x, y, linea)
        y -= line_spacing
    return y

def agregar_linea(c, x_inicio, x_fin, y):
    c.line(x_inicio, y, x_fin, y)

def crear_pdf(datos, ruta_pdf):
    c = canvas.Canvas(ruta_pdf, pagesize=A4)
    ancho, alto = A4
    margen = 50
    x_inicio = margen
    x_fin = ancho - 50
    y = alto - margen
    
    agregar_texto(c, datos['nombre_completo'].upper(), x_inicio, y, size=20, negrita=True, centrado=True)
    y -= 5
    agregar_linea(c, x_inicio, x_fin, y)
    y -= 15
    agregar_texto(c, datos['contacto'], x_inicio, y, size=12, centrado=True)
    y -= 30
    
    for seccion, contenido in datos.items():
        if seccion in ['educacion', 'experiencia', 'idiomas']:
            agregar_texto(c, seccion.upper(), x_inicio, y, size=14, negrita=True, centrado=True)
            y -= 20
            if y < 100:
                c.showPage()
                y = A4[1] - 50
            
            if isinstance(contenido, list):
                for item in contenido:
                    if isinstance(item, dict):
                        agregar_texto(c, item['titulo'], x_inicio, y, negrita=True)
                        c.drawRightString(x_fin, y, item['fecha'])  # Fecha alineada a la derecha
                        y -= 18
                        agregar_texto(c, item['institucion'], x_inicio, y, size=12)
                        y -= 18
                        for desc in item.get('descripcion', []):
                            y = agregar_texto_largo(c, f'• {desc}', x_inicio + 20, y, ancho_maximo=450)
                            y -= 8
                        y -= 15
                    else:
                        y = agregar_texto_largo(c, f'• {item}', x_inicio + 20, y, ancho_maximo=450)
                        y -= 8
            y -= 15
    
    agregar_pie_pagina(c)
    c.showPage()
    c.save()

if __name__ == "__main__":
    ruta_json = 'data.JSON'
    ruta_pdf = 'cv_generado_json.pdf'
    datos = cargar_datos_json(ruta_json)
    crear_pdf(datos, ruta_pdf)
    print(f'PDF generado exitosamente en: {ruta_pdf}')

# Ejecutar el script para generar el archivo PDF
# python pdfcreate.py


# python pdfcreate.py
