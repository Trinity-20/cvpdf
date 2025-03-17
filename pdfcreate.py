# Importar librerías necesarias
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
import json


def cargar_datos_json(ruta_json):
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    return datos


def agregar_texto_largo(c, texto, x_position, y_position, ancho_maximo, font_name="Helvetica", font_size=14, line_spacing=17):
    c.setFont(font_name, font_size)
    max_chars = int(ancho_maximo / (font_size * 0.4))  # Calcular número máximo de caracteres por línea
    lineas = wrap(texto, width=max_chars)

    for linea in lineas:
        if y_position < 50:
            #nueva_pagina(c)
            y_position = A4[1] - 50
            c.setFont(font_name, font_size)

        c.drawString(x_position, y_position, linea)
        y_position -= line_spacing

    return y_position


def agregar_pie_pagina(c):
    ancho, _ = A4
    c.setFont('Helvetica-Oblique', 12)
    pie_pagina = f'ESCUELA DE POSTGRADO DE LA UNAP - Página {c.getPageNumber()}'
    c.drawRightString(ancho - 50, 20, pie_pagina)


def agregar_marca_agua(c):
    ancho, alto = A4
    ancho_imagen = ancho * 1.9
    alto_imagen = alto * 1
    x_centrada = (ancho - ancho_imagen) / 2
    y_centrada = (alto - alto_imagen) / 2
    c.saveState()
    c.setFillAlpha(0.10)
    c.drawImage('20.png', x_centrada, y_centrada, ancho_imagen, alto_imagen, mask='auto')
    c.restoreState()

"""""
def nueva_pagina(c):
    agregar_pie_pagina(c)  # Añadir pie de página a la página actual
    c.showPage()  # Crear nueva página
    agregar_marca_agua(c)  # Añadir la marca de agua en la nueva página
"""""

def crear_pdf(datos, ruta_pdf):
    c = canvas.Canvas(ruta_pdf, pagesize=A4)
    ancho, alto = A4
    x_position = 50
    y_position = alto - 50

    agregar_marca_agua(c)  # Añadir marca de agua en la primera página

    # Encabezado
    c.setFont('Helvetica-Bold', 22)
    c.drawString(x_position, y_position, datos['nombre_completo'])
    y_position -= 20
    c.setFont('Helvetica', 14)
    c.drawString(x_position, y_position, datos['contacto'])
    y_position -= 25

    # Dibujar contenido del JSON
    secciones = ['perfil', 'experiencias', 'formaciones', 'cursos', 'habilidades', 'idiomas']
    for seccion in secciones:
        y_position -= 10
        c.setFont('Helvetica-Bold', 16)
        c.drawString(x_position, y_position, seccion.upper())
        y_position -= 5
        c.line(x_position, y_position, 500, y_position)
        y_position -= 20
        c.setFont('Helvetica', 14)

        contenido = datos.get(seccion, [])

        if isinstance(contenido, str):
            y_position = agregar_texto_largo(c, contenido, x_position, y_position, ancho_maximo=450)
            y_position -= 15

        elif isinstance(contenido, list):
            for item in contenido:
                if isinstance(item, dict):
                    for clave, valor in item.items():
                        if clave == "Actividades":
                            c.setFont('Helvetica-Bold', 14)
                            c.drawString(x_position + 20, y_position, 'Actividades:')
                            y_position -= 15
                            c.setFont('Helvetica', 14)
                            for actividad in valor:
                                c.drawString(x_position + 30, y_position, f'• {actividad}')
                                y_position -= 15
                        elif clave == "Logros":
                            c.setFont('Helvetica-Bold', 14)
                            c.drawString(x_position + 20, y_position, 'Logros:')
                            y_position -= 20
                            c.setFont('Helvetica', 14)
                            for logro in valor:
                                c.drawString(x_position + 30, y_position, f'✓ {logro}')
                                y_position -= 15
                        else:
                            y_position = agregar_texto_largo(c, f'{clave}: {valor}', x_position + 20, y_position, ancho_maximo=450)
                            y_position -= 5
                    y_position -= 5
                else:
                    y_position = agregar_texto_largo(c, f'- {item}', x_position + 20, y_position, ancho_maximo=450)
                    y_position -= 5

    #nueva_pagina(c)
    agregar_pie_pagina(c) # Añadir pie de página a la última página
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
