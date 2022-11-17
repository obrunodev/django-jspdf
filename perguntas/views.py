from django.shortcuts import render
from perguntas.models import Pergunta


def perguntas_list(request):
    """Lista as perguntas da plataforma."""
    if request.method == 'GET':
        perguntas = Pergunta.objects.all()
        context = {'perguntas': perguntas}
        return render(request, 'perguntas/list.html', context)
