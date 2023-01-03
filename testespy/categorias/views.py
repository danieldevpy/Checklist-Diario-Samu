from django.http import HttpResponse
from categorias.models import Unidade, Insumo, Carga


def insertChargeItem(request):
    unitys = Unidade.objects.all()
    items = Insumo.objects.all()
    for unity in unitys:
        for item in items:
            create = Carga(unity=unity, item=item, charge=0)
            create.save()
    return HttpResponse('Itens criados para todas unidades')