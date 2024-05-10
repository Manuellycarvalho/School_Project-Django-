from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.abre_index, name='abre_index'),
    path('enviar_login', views.enviar_login, name='enviar_login'),
    path('confirmar_cadastro', views.confirmar_cadastro, name='confirmar_cadastro'),
    path('salvar_turma', views.salvar_turma_nova, name='salvar_turma_nova'),
    path('cad_turma/<int:id_professor>', views.cad_turma, name='cad_turma'),
    path('lista_turma/<int:id_professor>', views.lista_turma, name='lista_turma'),

    path('ver_atividades', views.ver_atividades, name='ver_atividades'),

    path('salvar_atividade_nova', views.salvar_atividade_nova, name='salvar_atividade_nova'),
    path('exibe_lista', views.exibe_lista, name='exibe_lista_turmas_professor'),
    path('excluir_turma/<int:id>', views.excluir_turma, name='excluir_turma'),
    path('accounts/', include('django.contrib.auth.urls'))
]
