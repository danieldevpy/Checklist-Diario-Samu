from datetime import datetime
import os
from fpdf import FPDF

class PDFMensal(FPDF):
    def header(self):
        # Rendering logo:
        line_height = self.font_size * 2.5
        self.image("./templates/static/img/logo.png", 10, 8, 33)
        self.ln(line_height)
        self.set_font("Times", size=14)
        self.cell(0, 10, f"Relatório mensal da viatura {self.ambu}", new_x="LMARGIN",)
        self.ln(line_height)
    
    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("./templates/static/img/logo.png", 10, 8, 33)

        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def create_pdf_mensal(dados_viatura, dates, items):
    now = datetime.now()
    hr = now.strftime('%H-%M-%S')
    path = 'media/'
    name = f'pdf/{hr}.pdf'
    pdf = PDFMensal()

    pdf.ambu = dados_viatura.name + "/" + dados_viatura.placa
    pdf.add_page()

    # Define a fonte e o tamanho do texto
    pdf.set_font("Times", size=10)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(77, 77, 77)


    line_height = pdf.font_size * 2.5

    for ctg in items:
        pdf.set_fill_color(242, 242, 242)
        pdf.multi_cell(45, line_height, ctg, border=1,align="CENTER",
            new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)

        for x in range(int(dates['init']), int(dates['fim'])):
            pdf.multi_cell(10, line_height, str(x), border=1, align="CENTER",
                new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
        pdf.ln(line_height)
        pdf.set_fill_color(255, 255, 255)
        for insumo in items[ctg]:
            copy = insumo
            if len(insumo) > 30:
                insumo = insumo[0:30]+"..."

            pdf.multi_cell(45, line_height, insumo.lower().capitalize(), border=1,align="CENTER",
                new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
        
            for x in range(int(dates['init']), int(dates['fim'])):
                try:
                    item = items[ctg][copy][x]
                except:
                    item = " "
                    
                pdf.multi_cell(10, line_height, str(item), border=1, align="CENTER",
                    new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
            pdf.ln(line_height)

        pdf.ln(line_height)

    # Salva o PDF em um arquivo temporário
    pdf.output(path+name)
    return path+name

def crate_pdf_temporario(dados_preenchente, registers, date):
    # Crie o objeto HttpResponse com o cabeçalho PDF apropriado.

    now = datetime.now()
    hr = now.strftime('%H-%M-%S')
    path = 'media/'
    name = f'pdf/{hr}.pdf'
    #começando
    pdf = PDF()
    pdf.add_page()
 
    pdf.set_font("Times", size=12)
    for row in dados_preenchente:
        pdf.cell(0, 10, row, new_x="LMARGIN",)
        pdf.ln(5)
    pdf.ln(5)
    pdf.cell(0, 10, f'Checklist preenchido em: {date}', new_x="LMARGIN", align="C")
    pdf.ln(15)
    

    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4  # distribute content evenly

    columns = {}

    for register in registers:
        if not register['category'] in columns:
            columns[register['category']] = True
            pdf.ln(2)
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_fill_color(242, 242, 242)
            pdf.cell(0, 12, register['category'].upper(), new_y="NEXT", fill=True, align="C")
            pdf.ln(1)
            pdf.set_fill_color(255, 255, 255)
            pdf.set_draw_color(77, 77, 77)
            pdf.set_font("Times", size=10)
            pdf.cell(col_width/2)
            pdf.multi_cell(col_width + col_width/2, line_height, register['name'], border=1,
                new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
            pdf.multi_cell(col_width + col_width/2, line_height, register['value'], border=1,
                new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
        else:
            pdf.cell(col_width/2)
            pdf.multi_cell(col_width + col_width/2, line_height, register['name'], border=1,
                new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
            pdf.multi_cell(col_width + col_width/2, line_height, register['value'], border=1,
                new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size, fill=True)
        pdf.ln(line_height)


    pdf.output(path+name)
    return path+name
 