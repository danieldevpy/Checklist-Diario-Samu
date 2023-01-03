from django.contrib import admin
from .models import Categoria, Insumo, Carga, RegistrosDiario, Unidade, Viatura, RegistroItemDiario
import time

# Register your models here.


class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'usa', 'usb')
    list_editable = ('usa', 'usb')


class AdminItem(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    list_editable = ('category',)


class AdminUnity(admin.ModelAdmin):
    pass


class AdminChargeItem(admin.ModelAdmin):
    model = Carga
    list_display = ('item', 'get_name_category', 'charge', 'unity',)
    list_filter = ('unity', 'item__category__name',)
    list_editable = ('charge',)

    def get_name_category(self, obj):
        return obj.item.category.name

    get_name_category.admin_order_field = 'Category'  # Allows column order sorting
    get_name_category.short_description = 'Categoria'  # Renames column head

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(unity=request.user.unity)
        

class AdminRegisterItemDay(admin.ModelAdmin):
    list_display = ('item', 'carga', 'unidade', 'vtr', 'date')
    list_editable = ('date',)
    list_filter = ('date', 'vtr')
    search_fields = ('item__name', )


class AdminRegisterDay(admin.ModelAdmin):
    list_display = ('name', 'unity', 'viatura', 'km', 'acesso','pdf', 'pub_date')
    list_filter = ('unity', 'pub_date')
    search_fields = ('viatura__name', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(unity=request.user.unity)


class AdminVtr(admin.ModelAdmin):
    list_display = ('name', 'placa', 'unidade')
    list_filter = ('unidade',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(unidade=request.user.unity)


admin.site.register(Categoria, AdminCategory)
admin.site.register(Unidade, AdminUnity)
admin.site.register(Insumo, AdminItem)
admin.site.register(Carga, AdminChargeItem)
admin.site.register(RegistroItemDiario, AdminRegisterItemDay)
admin.site.register(RegistrosDiario, AdminRegisterDay)
admin.site.register(Viatura, AdminVtr)