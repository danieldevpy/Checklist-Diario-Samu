from django.views.generic.list import ListView
from .models import Categoria, Carga, RegistrosDiario, Viatura, RegistroItemDiario
from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime, date
from .pdf import some_view
from .models import Insumo


def index(request):
    if request.user.is_authenticated:
        user = request.user 
        if user.usa and user.usb:
            categorias = Categoria.objects.filter()
            last = RegistrosDiario.objects.filter(unity=user.unity).last()
        elif user.usa:
            categorias = Categoria.objects.filter(usa=True)
            last = RegistrosDiario.objects.filter(unity=user.unity, acesso='usa').last()
        elif user.usb:
            categorias = Categoria.objects.filter(usb=True)
            last = RegistrosDiario.objects.filter(unity=user.unity, acesso='usb').last()


        items = Carga.objects.filter(unity__name=user.unity).order_by('item__name')
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
            user = request.user
            acesso = 'usa'
            if user.usa:
                acesso = 'usa'
            elif user.usb:
                acesso = 'usb'
            
            pdf = some_view(user.unity)
            nome_completo = request.POST.get('nomecompleto')
            cargo = request.POST.get('cargo')
            unidade = user.unity
            _viatura = request.POST.get('select_viaturas')
            viatura = Viatura.objects.filter(id=_viatura).first()
            km = request.POST.get('km')
            create_register = RegistrosDiario(
                name=nome_completo, cargo=cargo, unity=unidade, acesso=acesso,
                viatura=viatura, km=km, pdf=pdf
            )
            create_register.save()
            print(nome_completo, cargo, unidade, viatura, km)
            items = Carga.objects.filter(unity__name=user.unity).order_by('item__name')
            for obj in items:
                carga = request.POST.get(str(obj.id))
                if carga is None:
                    carga = 0
                register_item = RegistroItemDiario(
                item=obj.item,
                carga=carga,
                unidade=user.unity,
                vtr=viatura
                )
                register_item.save()
                # respostas.append(f'{obj.item.category.name} {obj.item.name}, {obj.charge}, {request.POST.get(str(obj.id))} /n ')

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
                _mes = request.POST.get('mes')
                _ano = request.POST.get('ano')
                if _mes == '04' or _mes == '06' or _mes == '09' or _mes == '11':
                    day = 30
                elif _mes == '02':
                    day = 28
                _viatura = request.POST.get('select_viaturas')
                objects = RegistroItemDiario.objects.filter(vtr=_viatura, date__range=(date(int(_ano),int(_mes),1), date(int(_ano), int(_mes), day)))
                vtr = Viatura.objects.filter(unidade=user.unity, id=_viatura).first()
                registro_vtr = RegistrosDiario.objects.filter(viatura__id=_viatura, pub_date__range=(date(int(_ano),int(_mes),1), date(int(_ano), int(_mes), day)))
                # for registro in registro_vtr:
                #     print(registro.km, registro.pub_date)
                context['infosday'] =  zip([str(f'1 a {day}/{_mes}/{_ano}')], [vtr])
                
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