from django.contrib import admin

from perguntas.models import Pergunta, Resposta


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    pass


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    pass
