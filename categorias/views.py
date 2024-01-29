import json
from django.http import FileResponse
from .models import Categoria, Carga, RegistrosDiario, Viatura
from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from django.db.models import Q
from .pdf import crate_pdf_temporario, create_pdf_mensal
import os
import calendar

def index(request):
    if request.user.is_authenticated:
        user = request.user 
        if user.usa and user.usb:
            categorias = Categoria.objects.filter().order_by('name')
            last = RegistrosDiario.objects.filter(unity=user.unity).last()
            items = Carga.objects.filter(unity=user.unity).order_by('item__name')
        elif user.usa:
            categorias = Categoria.objects.filter(usa=True).order_by('name')
            last = RegistrosDiario.objects.filter(unity=user.unity, acesso='usa').last()
            items = Carga.objects.filter(unity=user.unity).order_by('item__name')
        elif user.usb:
            categorias = Categoria.objects.filter(usb=True).order_by('name')
            last = RegistrosDiario.objects.filter(unity=user.unity, acesso='usb').last()
            items = Carga.objects.filter(unity=user.unity, item__usb=True).order_by('item__name')

   
        viaturas = Viatura.objects.filter(unidade=user.unity, ativo=True)
        if last:
            last_check = last.pub_date.strftime('%d/%m/%Y as '  "%H:%M:%S")
        else:
            last_check = 'Nenhum'

        context = {
            'categorias': categorias,
            'items': items,
            'user': user,
            'last': last_check,
            'viaturas': viaturas
            }

        return render(request, 'index.html', context)
    else:
        return redirect('user/login/')


def finalizar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            all_categorias = None
            user = request.user
            # filter
            acesso = 'usa'
            if user.usa:
                acesso = 'usa'
                all_categorias = Categoria.objects.filter(usa=True).all()
            elif user.usb:
                acesso = 'usb'
                all_categorias = Categoria.objects.filter(usb=True).all()

            # get to form
            nome_completo = request.POST.get('nomecompleto')
            cargo = request.POST.get('cargo')
            unidade = user.unity
            _viatura = request.POST.get('select_viaturas')
            km = request.POST.get('km')

            to_json = []
            for category in all_categorias:
                if acesso == 'usb':
                    carga = Carga.objects.filter(unity=user.unity, item__category=category, item__usb=True).order_by('item__name')
                else:
                    carga = Carga.objects.filter(unity=user.unity, item__category=category).order_by('item__name')
                for obj in carga:
                    value = request.POST.get(str(obj.pk))
                    to_json.append({"id": obj.pk, "category": category.name, "name": obj.item.name, "value": value})

            # crate
            viatura = Viatura.objects.filter(id=_viatura).first()
            create_register = RegistrosDiario(
                name=nome_completo, cargo=cargo, unity=unidade, acesso=acesso,
                viatura=viatura, km=km, items=json.dumps(to_json)
            )
            create_register.save()

            context = {
            'dataatual': datetime.now().strftime('%d/%m/%Y as '  "%H:%M:%S"),
            'preenchente': nome_completo
            }
            return render(request, 'finalizado.html', context)
        else:
            context = {
            'dataatual': datetime.now().strftime('%d/%m/%Y as '  "%H:%M:%S"),
            'preenchente': "daniel"
            }
            return render(request, 'finalizado.html', context)

    else:
        return redirect('/')

def view_pdf(request, pk):
    register = RegistrosDiario.objects.filter(id=int(pk)).first()
    if not register:
        return False
    dados_preenchente = [f'Nome do Funcionário: {register.name}', f'Cargo: {register.cargo}', f'Unidade: {register.unity.name}', f'Viatura: {register.viatura.name}, Placa: {register.viatura.placa}, KM: {register.km}']
    registers = json.loads(register.items)
    pdf = crate_pdf_temporario(dados_preenchente, registers, register.pub_date.strftime('%d-%m-%Y às %H:%M'))
    pdf_file = open(pdf, "rb")
    os.remove(pdf)
    response = FileResponse(pdf_file)
    return response

def sugestao(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            json_data = request.body.decode('utf-8')
            # Decodifica o JSON para um objeto Python
            data = json.loads(json_data)
            preenchente = data.get('preenchente')
            sugestext = data.get('sugestText')
            # Sugestao(preenchente=preenchente, sugestao=sugestext).save()

            return HttpResponse(status=200)
        
def dashboard(request):
    return render(request, 'dashboard/dash.html',)

def dashboard_registros(request, pk, date, ano):
    print("x ano teste", ano)
    if ano == 0:
        ano = datetime.now().year
    user = request.user
    anos = [2023, 2024]
    meses = zip(range(1, 13), ["Janeiro", "Fevereiro", "Março", "Abril",  "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outrubro", "Novembro", "Dezembro"])
    viaturas = Viatura.objects.filter(unidade=user.unity, ativo=True).all()
    context = {"index": False, "viaturas": viaturas, "meses":meses, "mes": date, "vtr": pk, "anos": anos, "selectAno": ano}
    if pk == 0 or date == 0:
        context['index'] = True
    return render(request, 'dashboard/dash_registros_mensal.html', context)


def generate_pdf_r_mensal(request, pk, date, part, ano):
    print(f'o ano foi {ano}')
    inicio = 1
    ultimo_dia = 15+1
    if part == 1:
        inicio = 16
        _, ultimo_dia = calendar.monthrange(ano, date)

    viatura = Viatura.objects.filter(id=pk).first()
    data_inicial = datetime(ano, date, inicio)
    data_final = datetime(ano, date, ultimo_dia)
    consulta = Q(pub_date__gte=data_inicial, pub_date__lte=data_final, viatura=viatura)
    
    items = {}
    registers = RegistrosDiario.objects.filter(consulta).order_by("pub_date")
    if not registers:
        return HttpResponse(status=404)

    for register in registers:
        if not 'Km Preenchidos' in items:
            items['Km Preenchidos'] = {}
            items['Km Preenchidos'][viatura.name] = {}
        
        items['Km Preenchidos'][viatura.name][int(register.pub_date.strftime("%d"))] = register.km
        all_item = json.loads(register.items)
        for item in all_item:
            day = int(register.pub_date.strftime("%d"))

            ctg = item['category']
            name = item['name']
            value = item['value']
    
            if not ctg in items:
                items[ctg] = {}

            if not name in items[ctg]:
                items[ctg][name] = {}

            items[ctg][name][day] = value


    archive = create_pdf_mensal(viatura, {"init": inicio, "fim": ultimo_dia}, items)
    with open(archive, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="relatorio-mensal.pdf"'
    
    os.remove(archive)
    return response