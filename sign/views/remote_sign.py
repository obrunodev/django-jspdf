from django.shortcuts import render


def index(request):
    """Função principal"""
    context = {'section': 'INDEX'}
    return render(request, 'sign/index.html', context)
