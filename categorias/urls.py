from django.urls import path, include
from testespy.categorias.views import insertChargeItem
from categorias import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checklist/', views.index, name='index'),
    path('finalizar/', views.finalizar, name='finalizar'),
    path('user/', include('unity.urls'), name='user'),
    path('create_itemcharge/', insertChargeItem, name='t_create'),
    path('pdf/<int:pk>', views.view_pdf, name="pdf"),
    path("sugestao", views.sugestao, name='sugestao'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/r_mensal/<int:pk>/<int:date>/<int:ano>', views.dashboard_registros, name='registro_mensal'),
    path('generate_pdf_r_mensal/<int:pk>/<int:date>/<int:part>/<int:ano>', views.generate_pdf_r_mensal, name="g_r_mensal")
]