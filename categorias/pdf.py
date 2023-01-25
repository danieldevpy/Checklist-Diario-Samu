from datetime import datetime
import os
from fpdf import FPDF



class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("./templates/static/img/logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15
        # Moving cursor to the right:
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")



def crate_pdf(unidade, dados_preenchente, registros):
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
    pdf = PDF()
    pdf.add_page()
 
    pdf.set_font("Times", size=12)
    for row in dados_preenchente:
        pdf.cell(0, 10, row, new_x="LMARGIN",)
        pdf.ln(5)
    pdf.ln(5)
    pdf.cell(0, 10, f'Checklist preenchido em: {data}', new_x="LMARGIN", align="C")
    pdf.ln(15)
    

    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4  # distribute content evenly


    for category in registros:
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_fill_color(242, 242, 242)
        pdf.cell(0, 12, category.upper(), new_y="NEXT", fill=True, align="C")
        pdf.ln(1)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(77, 77, 77)
        pdf.set_font("Times", size=10)
        for row in registros[category]:
            pdf.cell(col_width/2)
            for datum in row:
                pdf.multi_cell(col_width + col_width/2, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
            pdf.ln(line_height)
        pdf.ln(2)


    pdf.output(path+name)
    return name
 