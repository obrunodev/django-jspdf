from django.shortcuts import get_object_or_404, redirect, render
from perguntas.forms import PerguntaForm, RespostaForm
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


def perguntas_responder(request, pergunta_id):
    """Função que apresenta respostas e responde a pergunta."""
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    if request.method == 'GET':
        form = RespostaForm()
        context = {'pergunta': pergunta,
                   'form': form}
        return render(request, 'perguntas/responder.html', context)
    
    if request.method == 'POST':
        form = RespostaForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.pergunta = pergunta
            obj.save()
            return redirect('perguntas:responder',
                            pergunta_id=pergunta.id)
