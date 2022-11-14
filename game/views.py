from django.shortcuts import render


def index(request):
    """Renderiza tela principal do game."""
    if request.method == 'GET':
        return render(request, 'game/index.html')
