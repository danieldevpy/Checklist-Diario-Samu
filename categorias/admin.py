from django.contrib import admin
from .models import Categoria, Insumo, Carga, RegistrosDiario, Unidade, Viatura
import time
from django.utils.html import format_html

# Register your models here.


class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'usa', 'usb')
    list_editable = ('usa', 'usb')


class AdminItem(admin.ModelAdmin):
    list_display = ('name', 'category', 'usa', 'usb')
    list_filter = ('category',)
    list_editable = ('category', 'usa', 'usb')
    search_fields = ('name', )


class AdminUnity(admin.ModelAdmin):
    search_fields = ('name',)

class AdminChargeItem(admin.ModelAdmin):
    model = Carga
    list_display = ('item', 'get_name_category', 'charge', 'unity',)
    list_filter = ( 'item__category__name',)
    list_editable = ('charge',)
    search_fields = ('unity__name', 'item__name')

    def get_name_category(self, obj):
        return obj.item.category.name

    get_name_category.admin_order_field = 'Category'  # Allows column order sorting
    get_name_category.short_description = 'Categoria'  # Renames column head

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(unity=request.user.unity)
    


class AdminRegisterDay(admin.ModelAdmin):
    list_display = ('name', 'unity', 'viatura', 'km', 'acesso','pdf', 'pub_date')
    search_fields = ('name', 'viatura__name', 'unity__name')
    readonly_fields = ('display_pdf_link',)  # Certifique-se de adicionar o campo readonly ao tuple

    def display_pdf_link(self, instance):
        if instance.pdf:
            url = instance.pdf  # Altere para o atributo correto do seu modelo
            return format_html('<a href="{}">{}</a>', url, url)
        else:
            return None

    display_pdf_link.short_description = 'PDF Link'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(unity=request.user.unity)


class AdminVtr(admin.ModelAdmin):
    list_display = ('name', 'placa', 'unidade')
    search_fields = ('name', 'unidade__name', 'placa')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(unidade=request.user.unity)


admin.site.register(Categoria, AdminCategory)
admin.site.register(Unidade, AdminUnity)
admin.site.register(Insumo, AdminItem)
admin.site.register(Carga, AdminChargeItem)
admin.site.register(RegistrosDiario, AdminRegisterDay)
admin.site.register(Viatura, AdminVtr)
