from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
import json

# Definir márgenes personalizados
MARGEN_IZQUIERDO = 50
MARGEN_DERECHO = 50
MARGEN_SUPERIOR = 50
MARGEN_INFERIOR = 50
ANCHO_UTIL = A4[0] - MARGEN_IZQUIERDO - MARGEN_DERECHO
ALTO_UTIL = A4[1] - MARGEN_SUPERIOR - MARGEN_INFERIOR

def cargar_datos_json(ruta_json):
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def agregar_pie_pagina(c):
    ancho, _ = A4
    c.setFont('Helvetica-Oblique', 9)
    c.drawString(MARGEN_IZQUIERDO, 20, "ESCUELA DE POSTGRADO DE LA UNAP")
    pie_pagina = f'Página {c.getPageNumber()}'
    c.drawRightString(ancho - MARGEN_DERECHO, 20, pie_pagina)

def agregar_texto(c, texto, x, y, font="Helvetica", size=12, negrita=False, centrado=False):
    c.setFont("Helvetica-Bold" if negrita else font, size)
    if centrado:
        x = (A4[0] - c.stringWidth(texto, "Helvetica-Bold" if negrita else font, size)) / 2
    c.drawString(x, y, texto)

def agregar_texto_largo(c, texto, x, y, ancho_maximo=ANCHO_UTIL, font_name="Helvetica", font_size=12, line_spacing=15):
    c.setFont(font_name, font_size)
    max_chars = int(ancho_maximo / (font_size * 0.5))
    lineas = wrap(texto, width=max_chars)
    for linea in lineas:
        if y < MARGEN_INFERIOR:
            c.showPage()
            y = A4[1] - MARGEN_SUPERIOR
            c.setFont(font_name, font_size)
        c.drawString(x, y, linea)
        y -= line_spacing
    return y

def agregar_linea(c, x_inicio, x_fin, y):
    c.line(x_inicio + MARGEN_IZQUIERDO, y, x_fin - MARGEN_DERECHO, y)

def crear_pdf(datos, ruta_pdf):
    c = canvas.Canvas(ruta_pdf, pagesize=A4)
    y = A4[1] - MARGEN_SUPERIOR  # Inicio del contenido respetando margen superior
    
    agregar_texto(c, datos['nombre_completo'].upper(), MARGEN_IZQUIERDO, y, size=20, negrita=True, centrado=True)
    y -= 5
    agregar_linea(c, MARGEN_IZQUIERDO, A4[0] - MARGEN_DERECHO, y)
    y -= 15
    agregar_texto(c, datos['contacto'], MARGEN_IZQUIERDO, y, size=12, centrado=True)
    y -= 30
    
    for seccion, contenido in datos.items():
        if seccion in ['educacion', 'experiencia', 'idiomas']:
            agregar_texto(c, seccion.upper(), MARGEN_IZQUIERDO, y, size=14, negrita=True, centrado=True)
            y -= 20
            if y < MARGEN_INFERIOR:
                c.showPage()
                y = A4[1] - MARGEN_SUPERIOR
            
            if isinstance(contenido, list):
                for item in contenido:
                    if isinstance(item, dict):
                        agregar_texto(c, item['titulo'], MARGEN_IZQUIERDO, y, negrita=True)
                        c.drawRightString(A4[0] - MARGEN_DERECHO, y, item['fecha'])  # Fecha alineada a la derecha
                        y -= 18
                        agregar_texto(c, item['institucion'], MARGEN_IZQUIERDO, y, size=12)
                        y -= 18
                        for desc in item.get('descripcion', []):
                            y = agregar_texto_largo(c, f'• {desc}', MARGEN_IZQUIERDO + 20, y)
                            y -= 8
                        y -= 15
                    else:
                        y = agregar_texto_largo(c, f'• {item}', MARGEN_IZQUIERDO + 20, y)
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
