from django.urls import path, include
from testespy.categorias.views import insertChargeItem
from categorias import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checklist/', views.index, name='index'),
    path('finalizar/', views.finalizar, name='finalizar'),
    path('registros/', views.registros_mensal, name='registros'),
    path('user/', include('unity.urls'), name='user'),
    path('create_itemcharge/', insertChargeItem, name='t_create'),
    path('pdf/<int:pk>', views.view_pdf, name="pdf")
]