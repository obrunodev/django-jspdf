import base64
import requests
import os
import json
import jwt

from datetime import date
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from docusign_esign import (RecipientViewRequest, EnvelopeDefinition, Document,
                            Signer, SignHere, Tabs, Recipients, ApiClient,
                            EnvelopesApi, Text, DateSigned, CarbonCopy, Envelope)
from project.settings import ACCOUNT_ID, BASE_DIR, CLIENT_AUTH_ID, CLIENT_USER_ID
from rest_framework.decorators import api_view
from sign import utils


@api_view(['POST'])
def docusign_signature(request):
    if request.method == 'POST':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                         'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            contractor_name = f"{request.POST.get('contractor_name')}"
            contractor_email = request.POST.get('contractor_email')
            hired_name = request.POST.get('hired_name')
            hired_email = request.POST.get('hired_email')
            witness_name = f"{request.POST.get('witness_name')}"
            witness_email = request.POST.get('witness_email')
            document_name = request.POST.get('document_name')
            document_file = request.FILES['document_file'].read()
            base64_file_content = base64.b64encode(document_file).decode('ascii')
            envelope_id = utils.signature_by_email(token, base64_file_content,
                                                   contractor_name, contractor_email,
                                                   hired_name, hired_email,
                                                   witness_name, witness_email,
                                                   document_name)
            url = ''
            return JsonResponse({'docusign_url': url,
                                 'envelope_id': envelope_id,
                                 'message': 'O envelope foi criado na Docusign',
                                 'error': ''})
        except Exception as e:
            return HttpResponse(f'Erro -> {str(e)}')
            # return JsonResponse({'docsign_url': '',
            #                     'envelope_id': '',
            #                     'message': 'Internal server error (docusign_signature)',
            #                     'error': str(e)})


@api_view(['GET'])
def get_envelope_status(request, envelope_id):
    if request.method == 'GET':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}'
            r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
            response = r.json()
            return JsonResponse(response)
        except Exception as error:
            return HttpResponse(str(error))


@api_view(['GET'])
def envelopes_list(request):
    """Lista todos os envelopes cadastrados no docusign."""
    if request.method == 'GET':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/search_folders/all/'
            # base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/search_folders/awaiting_my_signature'
            # base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/'
            # base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes?user_id=c6d82a85-d295-4b80-8655-7ce85922f411'
            r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
            response = r.json()
            return JsonResponse(response)
        except Exception as error:
            return HttpResponse(str(error))


@api_view(['GET'])
def envelope_recipients(request, envelope_id):
    "Recebe os assinantes de um envelope através de ID do envelope."
    if request.method == 'GET':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                        'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}/recipients'
            r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
            response = r.json()
            return JsonResponse(response)
        except Exception as error:
            return HttpResponse(str(error))


@api_view(['GET'])
def envelope_documents(request, envelope_id):
    """Lista os documentos de um envelope."""
    if request.method == 'GET':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                         'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}/documents'
            r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
            response = r.json()
            return JsonResponse(response)
        except Exception as error:
            return HttpResponse(str(error))


@api_view(['GET'])
def download_documents(request, envelope_id, document_id):
    """Baixa os documentos de um envelope."""
    if request.method == 'GET':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                         'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            api_client = utils.create_api_client('https://demo.docusign.net/restapi', token['access_token'])
            envelope_api = EnvelopesApi(api_client)
            temp_file = envelope_api.get_document(account_id=ACCOUNT_ID,
                                                  document_id=document_id,
                                                  envelope_id=envelope_id)
            file = open(temp_file, "rb")
            return FileResponse(file, as_attachment=True)  # Faz download do arquivo.
        except Exception as error:
            return HttpResponse(str(error))


@api_view(['GET'])
def download_all_documents(request, envelope_id):
    """Baixa os documentos de um envelope."""
    if request.method == 'GET':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                        'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            api_client = utils.create_api_client('https://demo.docusign.net/restapi', token['access_token'])
            envelope_api = EnvelopesApi(api_client)
            temp_file = envelope_api.get_document(account_id=ACCOUNT_ID,
                                                document_id="archive",
                                                envelope_id=envelope_id)
            file = open(temp_file, "rb")
            return FileResponse(file, as_attachment=True)  # Faz download do arquivo.
        except Exception as error:
            return HttpResponse(str(error))


@api_view(['POST'])
def envelope_cancel(request, envelope_id):
    """Altera o status do envelope para void (Cancelado).
    
    Args:
    * voidedReason: Motivo do cancelamento do contrato.
    """
    if request.method == 'POST':
        try:
            envelope_id = request.POST.get('envelope_id')
            voidedReason = request.POST.get('voidedReason')
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                         'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}'
            data = {
                "status": "voided",
                "voidedReason": voidedReason
            }
            r = requests.put(base_url, json=data, headers={'Authorization': 'Bearer ' + token['access_token']})
            response = r.json()
            return JsonResponse(response)
        except Exception as error:
            print(error)
            return HttpResponse(error)


@api_view(['GET'])
def get_user_id(request, user_email):
    """Recebe o user_id da Docusign passando o e-mail."""
    if request.method == 'GET':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                        'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            user_id = requests.get(f"https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/users?email={user_email}",
                                headers={'Authorization': 'Bearer ' + token['access_token']})
            return JsonResponse(user_id)
        except Exception as error:
            return HttpResponse(str(error))


@api_view(['GET'])
def docusign_completed(request):
    """Retorna uma resposta quando a assinatura estiver completa."""
    return HttpResponse("Assinatura concluída.")


# ↓ UTIL FUNCTIONS ↓
def create_jwt_grant_token():
    token = utils.docusign_token()
    return token
