import json
from django.http import FileResponse
from .models import Categoria, Carga, RegistrosDiario, Viatura, Sugestao
from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime
from .pdf import crate_pdf_temporario
import os


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
            return redirect('/')

    else:
        return redirect('/')

def registros_mensal(request):
        # if request.user.is_authenticated:
        #     user = request.user 
        #     viaturas = Viatura.objects.filter(unidade=user.unity, ativo=True)
        #     context = {
        #     'items': False,    
        #     'viaturas': viaturas
        #     }
        #     if request.method == 'POST':
        #         day = 31
        #         _mes = int(request.POST.get('mes'))
        #         _ano = int(request.POST.get('ano'))
        #         _copy_mes = None
        #         _copy_ano = _ano

        #         if _mes == 4 or _mes == 6 or _mes == 9 or _mes == 11:
        #             day = 30
        #         elif _mes == 2:
        #             day = 28

        #         if _mes == 12:
        #             _copy_mes = 1
        #             _copy_ano += 1
        #         else:
        #             _copy_mes = _mes + 1
            
        #         _viatura = request.POST.get('select_viaturas')
        #         objects = RegistroItemDiario.objects.filter(vtr=_viatura, date__range=(date(_ano, _mes, 1), date(_copy_ano, _copy_mes, 1))).all()
        #         vtr = Viatura.objects.filter(unidade=user.unity, id=_viatura).first()
        #         registro_vtr = RegistrosDiario.objects.filter(viatura__id=_viatura, pub_date__range=(date(_ano, _mes, 1), date(_copy_ano, _copy_mes, 1)))
        #         context['infosday'] =  zip([str(f'1/{_mes}/{_ano} a 1/{_copy_mes}/{_copy_ano}')], [vtr])
        #         if objects:
        #             for obj1 in objects:
        #                 obj1.date = int(str(obj1.date)[8:10])
        #             for obj2 in registro_vtr:
        #                 obj2.pub_date = int(str(obj2.pub_date)[8:10])
        #             context['objects'] = objects
        #             context['vtrs'] = registro_vtr
        #             context['days'] = day
        #         return render(request, 'registros.html', context)
        #     else:
        #         return render(request, 'registros.html', context)
        # else:
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
            Sugestao(preenchente=preenchente, sugestao=sugestext).save()

            return HttpResponse(status=200)