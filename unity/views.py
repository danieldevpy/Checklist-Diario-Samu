from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib import messages
# Create your views here.


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
                
    elif request.method == 'POST':
        loginx = request.POST.get('unity').lower()
        password = request.POST.get('password').lower()
        user = authenticate(username=loginx, password=password)
        
        if user:
            login_django(request, user)
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha incorretos!')
            return render(request, 'login.html')

def logout(request):

    logout_django(request)
    return redirect('/')
