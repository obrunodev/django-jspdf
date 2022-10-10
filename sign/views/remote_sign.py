import base64

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from docusign_esign import (RecipientViewRequest, EnvelopeDefinition, Document,
                            Signer, SignHere, Tabs, Recipients, ApiClient,
                            EnvelopesApi, Text, DateSigned, CarbonCopy)
from project.settings import ACCOUNT_ID, BASE_DIR, CLIENT_AUTH_ID, CLIENT_USER_ID


def index(request):
    """Função principal"""
    context = {'section': 'INDEX'}
    return render(request, 'sign/index.html', context)


@csrf_exempt
def make_envelope():
    """Cria um envelope na Docusign"""
    pass