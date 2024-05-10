from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages #Biblioteca de mensagens do Django

def initial_population():

    print("Vou Popular")

    cursor = connection.cursor()

    # Popular Tabela Professor
    senha = "123456"  # senha inicial para todos os usuarios
    senha_armazenar = sha256(senha.encode()).hexdigest()
    # Montamos aqui nossa instrução SQL.
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES "
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '" + senha_armazenar + "'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "')"

    cursor.execute(insert_sql_professor)
    transaction.atomic() # Necessario commit para insert e update
    # Fim da População da tabela Professor

    #---------------------------------------------------------------------------------------

    # Popular Tabela Turma
    # Montamos aqui nossa instrução SQL.
    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES "
    insert_sql_turma = insert_sql_turma + "('1o Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2o Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3o Semestre - Desenvolvimento de Sistemas', 3)"

    cursor.execute(insert_sql_turma)
    transaction.atomic()  # Necessario commit para insert e update

    # Fim da População da tabela Turma

    # ---------------------------------------------------------------------------------------
    # Popular Tabela Atividade
    # Montamos aqui nossa instrução SQL.
    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES "
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programção', 1),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de Gerenciamento de Projetos', 3)"

    cursor.execute(insert_sql_atividade)
    transaction.atomic()  # Necessario commit para insert e update

    # Fim da População da tabela Atividade

    print("Populei")

# Create your views here.
def abre_index(request):
    #return render(request, 'Index.html')
    # mensagem = "OLÁ TURMA, MUITO BOM DIA!"
    # return HttpResponse(mensagem)

    # query set Tipos de Look Up
    # nome__exact='SS' - tem que ser exatamente igual
    # nome__contains='H' - contem o H maiusculo
    # nome__icontains='H' - ignora se maiúsculo ou minúsculo
    # nome__startswith='M' - traz o que começa com a letra M ou sequencia de letras
    # nome__istartswith='M' - traz o que começa com a letra M ignorando se maiusculo ou minusculo u sequencia de letras
    # nome__endswith='a' - traz o que termina com a letra a minusculo ou sequencia de letras
    # nome__iendswith='a' - traz o que termina com a letra a ignorando maiúsculo ou minusculo
    # nome__in=['Michael', 'Obama']) traz somente os nome que estão na lista
    # Pode ser feito uma composição 'and' utilizando , (virgula entre os campos) ou 'or' utilizando | (pipe entre os campos)

    dado_pesquisa = 'Obama'

    verifica_populado = Professor.objects.filter(nome__icontains=dado_pesquisa)
    #verifica_populado = Professor.objects.filter(nome='Prof. Barak Obama')

    if len(verifica_populado) == 0:
       print ("Não está Populado")
       initial_population()
    else:
        print ("Achei Obama ", verifica_populado)

    usuario_logado = request.user.username

    return render(request, 'index.html', {'usuario_logado': usuario_logado})
        

    # return render(request, 'login.html')

def enviar_login(request):

    if (request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")
        print ("Dados do Professor ", dados_professor)
        #if len(dados_professor) > 0:
        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            if (senha == senha_criptografada):
                messages.info(request, 'Bem vindo.')

                # mensagem = "OLÁ PROFESSOR, " + email + " . SEJA BEM VINDO!!!"
                # return HttpResponse(mensagem)

                # Se logou corretamente, traz as turmas do professor
                # Para isso instanciamos o model turmas do professor
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
                print("Turma do Professor ", turmas_do_professor)
                return render(request, 'Cons_Turma_Lista.html',
                              {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor,
                               'id_logado': id_logado})



            else:
                messages.info(request, 'Usuario ou senha incorretos. Tente novamente.')
                return render(request, 'login.html')

        messages.info(request, "Olá " + email + ", seja bem-vindo! Percebemos que você é novo por aqui. "
                                                "Complete o seu cadastro.")
        return render(request, 'cadastro.html', {'login': email})

def confirmar_cadastro(request):
    if (request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        grava_professor = Professor(
            nome=nome,
            email=email,
            senha=senha_criptografada
        )
        grava_professor.save()

        mensagem = "OLÁ PROFESSOR " + nome + ", SEJA BEM VINDO!"
        return HttpResponse(mensagem)

        #Se desejar que a resposta seja uma pagina, substitua a linha acima pela linha abaixo
        #indicando a página para ser exibida
        #return render(request, 'Pagina_Resposta.html')

def cad_turma(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']
    #print (usuario_logado, " USUARIO LOGADO EM CAD_CLIENTE")
    return render(request, 'Cad_Turma.html', {'usuario_logado': usuario_logado, 'id_logado': id_professor })
    #return render(request, 'Cad_Cliente.html')

def salvar_turma_nova(request):

    if (request.method == 'POST'):
        nome_turma = request.POST.get('nome_turma')
        id_professor = request.POST.get('id_professor')

        professor = Professor.objects.get(id=id_professor)

        grava_turma = Turma(
            nome_turma=nome_turma,
            id_professor=professor
        )
        grava_turma.save()
        messages.info(request, 'Turma ' + nome_turma + ' cadastrado com sucesso.')

        dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
        usuario_logado = dados_professor[0]
        usuario_logado = usuario_logado['nome']
        id_logado = dados_professor[0]
        id_logado = id_logado['id']
        turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
        #return render(request, 'Cad_Cliente.html',{'usuario_logado': usuario_logado})
        return render(request, 'Cons_Turma_Lista.html', {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor, 'id_logado': id_logado})

def lista_turma(request, id_professor):

    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
    # return render(request, 'Cad_Cliente.html',{'usuario_logado': usuario_logado})
    return render(request, 'Cons_Turma_Lista.html',
                  {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor,
                   'id_logado': id_logado})



def ver_atividades(request):

    id_turma = request.GET.get('id_turma')
    id_logado = request.GET.get('who')
    nome_da_turma = Turma.objects.get(id=id_turma)

    dados_professor = Professor.objects.filter(id=id_logado).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    #id_logado = dados_professor[0]
    #id_logado = id_logado['id']
    atividades_da_turma = Atividade.objects.filter(id_turma=id_turma)

    # return render(request, 'Cad_Cliente.html', {'usuario_logado': usuario_logado})
    return render(request, 'Cons_Turma_Atividade.html',
                  {'usuario_logado': usuario_logado,
                   'atividades_da_turma': atividades_da_turma,
                   'id_logado': id_logado,
                   'nome_da_turma': nome_da_turma})


def salvar_atividade_nova(request):

    if (request.method == 'POST'):
        nome_atividade = request.POST.get('nome_atividade')
        id_turma = request.POST.get('id_turma')
        id_logado = request.POST.get('id_professor')

        turma = Turma.objects.get(id=id_turma)

        grava_atividade = Atividade(
            nome_atividade=nome_atividade,
            id_turma= turma
        )
        grava_atividade.save()
        messages.info(request, 'Atividade ' + nome_atividade + ' cadastrado com sucesso.')

        nome_da_turma = Turma.objects.get(id=id_turma)

        dados_professor = Professor.objects.filter(id=id_logado).values("nome", "id")
        usuario_logado = dados_professor[0]
        usuario_logado = usuario_logado['nome']

        atividades_da_turma = Atividade.objects.filter(id_turma=id_turma)

        return render(request, 'Cons_Turma_Atividade.html',
                      {'usuario_logado': usuario_logado,
                       'atividades_da_turma': atividades_da_turma,
                       'id_logado': id_logado,
                       'nome_da_turma': nome_da_turma})


def excluir_turma(request, id ):

    #A identificação do professor deve ser feita aqui antes de excluir a turma
    #pois se for realizado depois de excluir a turma, não conseguimos identificar o professor
    id_professor = Turma.objects.filter(id=id).values('id_professor')
    id_professor = id_professor[0]
    id_professor = id_professor['id_professor']

    atividades_na_turma = Atividade.objects.filter(id_turma=id)

    # Verifica se há atividades cadastrada para a turma. Caso existe não permite e exclusão
    if atividades_na_turma:
        messages.info(request, 'Já existe atividades cadastradas para essa turma. Ela não pode ser excluída.')
    else:

       turma_a_excluir =  get_object_or_404(Turma, pk=id)
       turma = turma_a_excluir.nome_turma
       turma_a_excluir.delete()

       messages.info(request, 'Turma ' + turma + ' excluída com sucesso.')


    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    turmas_do_professor = Turma.objects.filter(id_professor=id_professor)
    return render(request, 'Cons_Turma_Lista.html',
                 {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor, 'id_logado': id_professor})


def exibe_lista(request):
    id_logado = request.GET.get('who')
    id_logado = Professor.objects.filter(id=id_logado).values("nome", "id")
    # Se logou corretamente, traz os clientes do vendedor
    # Para isso instanciamos o model clientes do Vendedor
    id_logado =  id_logado[0]
    usuario_logado = id_logado['nome']
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
    # print(turmas_do_vendedor)
    # return render(request, 'Cons_Turma_Lista_V.html', {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor})
    return render(request, 'Cons_Turma_Lista.html',
                  {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor, 'id_logado': id_logado})
    # return render(request, 'Cons_Turma_Atividade.html')

