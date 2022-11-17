from django.contrib import admin

from perguntas.models import Pergunta


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    pass
