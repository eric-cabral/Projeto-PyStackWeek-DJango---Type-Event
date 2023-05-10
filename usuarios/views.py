from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib import auth

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais!')
            return redirect(reverse('cadastro'))
        
        # TODO: Validar força da senha
        while True:
            if senha.islower():
                messages.add_message(request, constants.WARNING, 'A senha deve ter pelo menos um caractere maiúsculo')
                return redirect(reverse('cadastro'))
            elif len(senha) < 7:
                messages.add_message(request, constants.WARNING, 'A senha deve ter pelo menos 8 caracteres!')
                return redirect(reverse('cadastro'))
            elif senha.isalpha():
                messages.add_message(request, constants.WARNING, 'Necessita de um número!')
                return redirect(reverse('cadastro'))
            elif senha.isalnum():
                messages.add_message(request, constants.WARNING, 'Necessita de um caractere especial!')
                return redirect(reverse('cadastro'))
            else:
                break

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já cadastrado!')
            return redirect(reverse('cadastro'))

        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, 'CADASTRO REALIZADO COM SUCESSO!!!')

        return redirect(reverse('login'))


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect(reverse('login'))
        
        auth.login(request, user)

        return redirect('/eventos/novo_evento/')
    