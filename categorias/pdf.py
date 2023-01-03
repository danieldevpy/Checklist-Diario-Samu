from io import StringIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os

def some_view(unidade):
    # Crie o objeto HttpResponse com o cabeçalho PDF apropriado.

    now = datetime.now()
    data = now.strftime('%d-%m-%Y')
    hr = now.strftime('%H-%M-%S')
    path = 'media/'
    name = f'pdf/{data}/{str(unidade)}-{hr}.pdf'
    exist = os.path.exists(f'{path}/pdf/{data}')
    if not exist:
        os.mkdir(f'{path}/pdf/{data}')


    #começando
    pdf = canvas.Canvas(path+name)
    pdf.drawString(100, 100, "Primeira página")
    pdf.showPage()

    pdf.drawString(200, 100, "Segunda página")

    pdf.drawString(300, 100, "Terceira página")
    pdf.showPage()

    pdf.save()
    print(name)
    return name
 