from django.views.generic.list import ListView
from .models import Categoria, Carga, RegistrosDiario, Viatura, RegistroItemDiario
from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime, date
from .pdf import crate_pdf
from .models import Insumo


def index(request):
    if request.user.is_authenticated:
        user = request.user 
        if user.usa and user.usb:
            categorias = Categoria.objects.filter().order_by('name')
            last = RegistrosDiario.objects.filter(unity=user.unity).last()
        elif user.usa:
            categorias = Categoria.objects.filter(usa=True).order_by('name')
            last = RegistrosDiario.objects.filter(unity=user.unity, acesso='usa').last()
        elif user.usb:
            categorias = Categoria.objects.filter(usb=True).order_by('name')
            last = RegistrosDiario.objects.filter(unity=user.unity, acesso='usb').last()


        items = Carga.objects.filter(unity=user.unity).order_by('item__name')
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
            respostas = []
            all_categorias = None
            all_registros = {}
            dados_preenchente = None
            user = request.user
            acesso = 'usa'
            if user.usa:
                acesso = 'usa'
                all_categorias = Categoria.objects.filter(usa=True).all()
            elif user.usb:
                acesso = 'usb'
                all_categorias = Categoria.objects.filter(usb=True).all()



            nome_completo = request.POST.get('nomecompleto')
            cargo = request.POST.get('cargo')
            unidade = user.unity
            _viatura = request.POST.get('select_viaturas')
            viatura = Viatura.objects.filter(id=_viatura).first()
            placa = viatura.placa
            km = request.POST.get('km')
            dados_preenchente = [f'Nome do Funcionário: {nome_completo}', f'Cargo: {cargo}', f'Unidade: {unidade.name}', f'Viatura: {viatura.name}, Placa: {placa}, KM: {km}']
            print(unidade)
            for category in all_categorias:
                all_registros[category.name] = []
                carga = Carga.objects.filter(unity=user.unity, item__category=category).order_by('item__name')
                for obj in carga:
                    value = request.POST.get(str(obj.id))
                    all_registros[category.name].append((obj.item.name, value))
                    register_item = RegistroItemDiario(
                    item=obj.item,
                    carga=value,
                    unidade=user.unity,
                    vtr=viatura
                    )
                    register_item.save()


            pdf = crate_pdf(user.unity.name, dados_preenchente, all_registros)
            create_register = RegistrosDiario(
                name=nome_completo, cargo=cargo, unity=unidade, acesso=acesso,
                viatura=viatura, km=km, pdf=pdf
            )
            create_register.save()

            datax = datetime.now().strftime('%d/%m/%Y as '  "%H:%M:%S")
            context = {
            'dataatual': datax
            }
            return render(request, 'finalizado.html', context)


def registros_mensal(request):
        if request.user.is_authenticated:
            user = request.user 
            viaturas = Viatura.objects.filter(unidade=user.unity, ativo=True)
            context = {
            'items': False,    
            'viaturas': viaturas
            }

            if request.method == 'POST':
                day = 31
                _mes = int(request.POST.get('mes'))
                _ano = int(request.POST.get('ano'))
                _copy_mes = None
                _copy_ano = _ano

                if _mes == 4 or _mes == 6 or _mes == 9 or _mes == 11:
                    day = 30
                elif _mes == 2:
                    day = 28

                if _mes == 12:
                    _copy_mes = 1
                    _copy_ano += 1
                else:
                    _copy_mes = _mes + 1

                _viatura = request.POST.get('select_viaturas')
                objects = RegistroItemDiario.objects.filter(vtr=_viatura, date__range=(date(_ano, _mes, 1), date(_copy_ano, _copy_mes, 1)))
                vtr = Viatura.objects.filter(unidade=user.unity, id=_viatura).first()
                registro_vtr = RegistrosDiario.objects.filter(viatura__id=_viatura, pub_date__range=(date(_ano, _mes, 1), date(_copy_ano, _copy_mes, 1)))
                print(registro_vtr)
                # for registro in registro_vtr:
                #     print(registro.km, registro.pub_date)
                context['infosday'] =  zip([str(f'1/{_mes}/{_ano} a 1/{_copy_mes}/{_copy_ano}')], [vtr])

                if objects:
                    for obj1 in objects:
                        obj1.date = str(obj1.date)[8:10]

                    for obj2 in registro_vtr:
                        obj2.pub_date = str(obj2.pub_date)[8:10]

                    categorias = Categoria.objects.all()
                    items = Carga.objects.filter(unity=user.unity).all()
                    context['categorias'] = categorias
                    context['items'] = items
                    context['objects'] = objects
                    # for obj in context['objects']:
                    #     print(obj.date)
                    context['vtrs'] = registro_vtr
                    context['range'] = [str(dia) for dia in range(1, day+1)]
                    # range(1, day+1)
                return render(request, 'registros.html', context)
            else:
                return render(request, 'registros.html', context)