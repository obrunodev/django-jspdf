from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """Função principal"""
    context = {'section': 'INDEX'}
    return render(request, 'sign/index.html', context)


@csrf_exempt
def test_return(request):
    """Função para testes"""
    return {'Nome': 'Bruno', 'sobrenome': 'Pianca'}
