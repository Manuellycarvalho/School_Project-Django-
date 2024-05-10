from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

@login_required
def formulario_novo_user(request):
    return render(request, 'Cad_User.html')
    
    
@login_required
def salvar_usuario(request):
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    if usuario != None and usuario != "" and email != None and email != '' and senha != None and senha != '':
        try:
            tem_usuario = User.objects.get(username = usuario)

            if tem_usuario:
                messages.info(request, 'Usuario ' + usuario + 'ja existente no sistema. Tente outro nome.')
                return render(request, 'Cad_User.html')
    
        except User.DoesNotExist:
            dados_usuario = User.objects.create_user(username = usuario, email = email, password = senha)
            dados_usuario.save()
            messages.info(request, 'usuario ' + usuario + 'cadastradp com sucesso.')

            return render(request, 'Cad_User.html')
