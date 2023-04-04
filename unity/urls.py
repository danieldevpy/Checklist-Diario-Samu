from django.urls import path
from unity import views

urlpatterns = [
    path('login/', views.login, name='index_login'),
    path('logout/', views.logout, name='logout'),
]