from django.shortcuts import render


def perguntas_list(request):
    """Lista as perguntas da plataforma."""
    if request.method == 'GET':
        return render(request, 'perguntas/list.html')
