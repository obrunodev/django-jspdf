from django.shortcuts import redirect, render
from perguntas.forms import PerguntaForm
from perguntas.models import Pergunta


def perguntas_list(request):
    """Lista as perguntas da plataforma."""
    if request.method == 'GET':
        perguntas = Pergunta.objects.all()
        context = {'perguntas': perguntas}
        return render(request, 'perguntas/list.html', context)


def perguntas_create(request):
    """Renderiza formulário de pergunta e cria a pergunta no banco."""
    if request.method == 'GET':
        form = PerguntaForm()
        context = {'form': form}
    
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perguntas:list')
        context = {'form': form}
    
    return render(request, 'perguntas/create.html', context)
