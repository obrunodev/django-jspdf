# import base64
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sign import utils
# from docusign_esign import (RecipientViewRequest, EnvelopeDefinition, Document,
#                             Signer, SignHere, Tabs, Recipients, ApiClient,
#                             EnvelopesApi, Text, DateSigned, CarbonCopy)
# from project.settings import ACCOUNT_ID, BASE_DIR, CLIENT_AUTH_ID, CLIENT_USER_ID


def index(request):
    """Função principal"""
    context = {'section': 'INDEX'}
    return render(request, 'sign/index.html', context)


@csrf_exempt
def make_envelope(request):
    """Função de testes"""
    if request.method == 'POST':
        teste = request.POST.get('teste')
        return JsonResponse({"msg": teste})
    else:
        return JsonResponse({"msg": "Erro"})
