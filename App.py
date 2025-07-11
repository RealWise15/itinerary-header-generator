from flask import Flask, request, send_file, render_template, jsonify
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import webbrowser
from threading import Timer
import io
import os
import fitz  # PyMuPDF
import signal

app = Flask(__name__)
# Obtener la ruta del directorio del script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


#TAMANIO_PERSONALIZADO = (595, 937)  # 595 puntos de ancho y 842 puntos de alto POR DEFECTO


def agregar_texto_multilinea_centrado(c, texto, y, font_size, line_height):
    lines = texto.split('\n')
    page_width, _ = TAMANIO_PERSONALIZADO
    for line in lines:
        text_width = c.stringWidth(line, "Helvetica", font_size)
        x = (page_width - text_width) / 2
        c.drawString(x, y, line)
        y -= line_height


def crear_membrete_y_pie_pdf(ruta_imagen_membrete, ruta_imagen_logo, ruta_imagen_pie, texto_membrete, texto_pie):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=TAMANIO_PERSONALIZADO)
    page_width, page_height = TAMANIO_PERSONALIZADO

    # Dibujar membrete, logo y pie de página en el PDF
    c.drawImage(ruta_imagen_membrete, 0, page_height - 100, width=page_width, height=100)
    c.drawImage(ruta_imagen_logo, 440, page_height - 205, width=130, height=100)
    c.drawImage(ruta_imagen_pie, 100, 5, width=412, height=23)

    # Añadir texto al membrete
    c.setFont("Helvetica", 14)
    text_membrete_y = page_height - 120
    agregar_texto_multilinea_centrado(c, texto_membrete, text_membrete_y, font_size=14, line_height=14)


    '''# Dibujar un rectángulo blanco debajo del logo
    c.setFillColorRGB(0.5, 0.5, 0.5)
    rect_x = 295
    rect_y = 750
    rect_width = page_width - 10
    rect_height = 40
    c.rect(rect_x, rect_y, rect_width, rect_height, stroke=0, fill=1)'''
    
    # Dibujar un rectángulo blanco en el pie de página
    c.setFillColorRGB(1, 1, 1)
    rect_x = 25
    rect_y = 40
    rect_width = page_width - 50
    rect_height = 110
    c.rect(rect_x, rect_y, rect_width, rect_height, stroke=0, fill=1)

    # Añadir texto al pie
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 8)
    text_pie_y = 120
    agregar_texto_multilinea_centrado(c, texto_pie, text_pie_y, font_size=8, line_height=10)

    c.save()
    packet.seek(0)
    return packet


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    pdf_file = request.files['pdf']
    if not pdf_file:
        return jsonify({'message': 'No PDF uploaded'}), 400

    template = request.form['template']
    if not template:
        return jsonify({'message': 'No template selected'}), 400
    
    templatePlat = request.form['templatePlat']
    if not template:
        return jsonify({'message': 'No template selected'}), 400
    
    # Definir tamaño y desplazamiento según la plantilla seleccionada
    global TAMANIO_PERSONALIZADO, desplazamiento
    if templatePlat == 'templateA':
        TAMANIO_PERSONALIZADO = (595, 937)  # CARNIVAL
        desplazamiento = 95
    elif templatePlat == 'templateB':
        TAMANIO_PERSONALIZADO = (595, 975)  # HUB
        desplazamiento = 133
    else:
        # Opcional: manejar otros casos o un tamaño por defecto
        TAMANIO_PERSONALIZADO = (595, 842)  # Por defecto
        desplazamiento = 0
    # Verificar qué opción fue seleccionada
    # Tamaño personalizado (ancho, alto) en puntos
    #if 'templateA' in request.form:
        #TAMANIO_PERSONALIZADO = (595, 937)  # 595 puntos de ancho y 937 puntos de alto CARNIVAL
        #desplazamiento = 95
    #elif 'templateB' in request.form:
    #TAMANIO_PERSONALIZADO = (595, 962)  # 595 puntos de ancho y 962 puntos de alto HUB
    #desplazamiento = 120

    # Obtener fecha y hora actuales
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Mapeo de logos según la plantilla seleccionada
    logo_mapping = {
        'template1': (os.path.join(BASE_DIR, "static/logos/aa-logo.jpg")),
        'template2': (os.path.join(BASE_DIR, "static/logos/Aeromexico-Logo.jpg")),
        'template3': (os.path.join(BASE_DIR, "static/logos/Air-Airlines-Logo.jpg")),
        'template4': (os.path.join(BASE_DIR, "static/logos/Air-Canada-logo.jpg")),
        'template5': (os.path.join(BASE_DIR, "static/logos/Air-Europa-Logo.jpg")),
        'template6': (os.path.join(BASE_DIR, "static/logos/Air-France-Logo.jpg")),
        'template7': (os.path.join(BASE_DIR, "static/logos/Andes-Logo.jpg")),
        'template8': (os.path.join(BASE_DIR, "static/logos/Arajet-Logo.jpg")),
        'template9': (os.path.join(BASE_DIR, "static/logos/Avianca-logo.jpg")),
        'template10': (os.path.join(BASE_DIR, "static/logos/Boa-Logo.jpg")),
        'template11': (os.path.join(BASE_DIR, "static/logos/Copa-Airlines-logo.jpg")),
        'template12': (os.path.join(BASE_DIR, "static/logos/Delta-Airlines-Logo.jpg")),
        'template13': (os.path.join(BASE_DIR, "static/logos/Ethiopian-Logo.jpg")),
        'template14': (os.path.join(BASE_DIR, "static/logos/Etihad-Airways-Logo.jpg")),
        'template15': (os.path.join(BASE_DIR, "static/logos/Gol-Logo.jpg")),
        'template16': (os.path.join(BASE_DIR, "static/logos/Iberia-Logo.jpg")),
        'template17': (os.path.join(BASE_DIR, "static/logos/ITA-Airways-Logo.jpg")),
        'template18': (os.path.join(BASE_DIR, "static/logos/Jet-smart-logo.jpg")),
        'template19': (os.path.join(BASE_DIR, "static/logos/KLM-Logo.jpg")),
        'template20': (os.path.join(BASE_DIR, "static/logos/LATAM-Logo.jpg")),
        'template21': (os.path.join(BASE_DIR, "static/logos/Qatar-Airways-Logo.jpg")),
        'template22': (os.path.join(BASE_DIR, "static/logos/SA-Airways-Logo.jpg")),
        'template23': (os.path.join(BASE_DIR, "static/logos/Sky-Airline-Logo.jpg")),
        'template24': (os.path.join(BASE_DIR, "static/logos/Turkish-Airlines-Logo.jpg")),
        'template25': (os.path.join(BASE_DIR, "static/logos/United-Airlines-Logo.jpg")),
    }
   
    ruta_imagen_logo = logo_mapping.get(template, os.path.join(BASE_DIR, "static/fnet-logoOld.jpg"))

    ruta_imagen_membrete = os.path.join(BASE_DIR, 'static/membrete1.png')
    ruta_imagen_pie = os.path.join(BASE_DIR, 'static/pie1.png')

    texto_membrete = "ELECTRONIC TICKET\nPASSENGER ITINERARY/RECEIPT"
    texto_pie = """EL BOLETO QUE UD HA ADQUIRIDO ES:
    ** NO REEMBOLSABLE: DE NO SER UTILIZADO, PIERDE SU VALOR SIN RESPONSABILIDAD
    PARA LA AGENCIA NI PARA LA LINEA AÉREA.
    ** NO TRANSFERIBLE: NO PUEDE SER UTILIZADO POR PERSONA DISTINTA AL TITULAR
    ** NO MODIFICABLE: PARA CUALQUIER CAMBIO DE FECHA, HORA, RUTA, ESTARÁ SUJETO A
    ALGUNA PENALIDAD O, EN SU DEFECTO, A LA IMPOSIBILIDAD DE MODIFICACIÓN ALGUNA
    DEPENDIENDO DE LAS CONDICIONES DE LA TARIFA PUBLICADA.
    **********************************************************************
    POR FAVOR, PRESENTARSE EN EL AEROPUERTO 3 HORAS ANTES DE LA SALIDA DE SU VUELO"""

    # Crear el PDF con el membrete, logo y pie de página
    membrete_pie_pdf = crear_membrete_y_pie_pdf(ruta_imagen_membrete, ruta_imagen_logo, ruta_imagen_pie, texto_membrete, texto_pie)

    # Usar PyMuPDF (fitz) para cargar y modificar el PDF original
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        mediabox = page.mediabox
        mediabox.y1 += desplazamiento  # Ajuste para mover el contenido hacia abajo
        page.set_mediabox(mediabox)

    # Guardar el PDF modificado en memoria
    modified_pdf = io.BytesIO()
    doc.save(modified_pdf)
    doc.close()
    modified_pdf.seek(0)

    # Leer el PDF modificado con PyPDF2 y añadir el membrete y pie de página
    reader = PdfReader(modified_pdf)
    writer = PdfWriter()

    membrete_pie_reader = PdfReader(membrete_pie_pdf)
    membrete_pie_page = membrete_pie_reader.pages[0]

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page.merge_page(membrete_pie_page)
        writer.add_page(page)

    output_pdf = io.BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)

    # Generar el nombre del archivo final con la fecha y hora actuales
    file_name = f'Itinerario_vuelo_{current_time}.pdf'

    return send_file(output_pdf, as_attachment=True, download_name=file_name)

    
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Servidor Flask cerrado'

def shutdown_server():
    os.kill(os.getpid(), signal.SIGTERM)

def open_browser():
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    if os.path.exists(chrome_path):
        webbrowser.get(chrome_path).open_new("http://127.0.0.1:5000")
    else:
        webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=False)


