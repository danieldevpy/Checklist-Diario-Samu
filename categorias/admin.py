from django.contrib import admin
from .models import Categoria, Insumo, Carga, RegistrosDiario, Unidade, Viatura, Sugestao
import time
from django.urls import reverse
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
    fields = ['name', 'cargo', 'unity', 'acesso', 'viatura', 'km', 'pdf_link', 'pub_date']
    list_display = ('name', 'unity', 'viatura', 'km', 'pdf_link', 'pub_date')
    search_fields = ('name', 'viatura__name', 'unity__name')

    readonly_fields = ['pdf_link']
        
    def pdf_link(self, obj):
        url = reverse('pdf', args=[obj.pk])  # Substitua 'pdf_view' pelo nome da sua view de PDF
        return format_html('<a href="{}" target="_blank">{}</a>', url, "Visualizar PDF")

    
    pdf_link.short_description = 'LINK PARA VISUALIZAR O PDF'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(unity=request.user.unity)

class AdminSugestao(admin.ModelAdmin):
    list_display = ('preenchente', 'sugestao')


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
admin.site.register(Sugestao, AdminSugestao)
