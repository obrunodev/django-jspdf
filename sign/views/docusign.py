import base64
import requests
import os
import json
import jwt

from datetime import date
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from docusign_esign import (RecipientViewRequest, EnvelopeDefinition, Document,
                            Signer, SignHere, Tabs, Recipients, ApiClient,
                            EnvelopesApi, Text, DateSigned, CarbonCopy)
from project.settings import ACCOUNT_ID, BASE_DIR, CLIENT_AUTH_ID, CLIENT_USER_ID
from rest_framework.decorators import api_view
from sign import utils


@api_view(['POST'])
@csrf_exempt
def docusign_signature(request):
    if request.method == 'POST':
        try:
            token = create_jwt_grant_token()
            post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                         'assertion': token}
            base_url = 'https://account-d.docusign.com/oauth/token'
            r = requests.post(base_url, data=post_data)
            token = r.json()
            contractor_name = f"{request.POST.get('contractor_name')} {request.POST.get('contractor_surname')}"
            contractor_email = request.POST.get('contractor_email')
            hired_name = request.POST.get('hired_name')
            hired_email = request.POST.get('hired_email')
            witness_name = f"{request.POST.get('witness_name')} {request.POST.get('witness_surname')}"
            witness_email = request.POST.get('witness_email')
            document_name = request.POST.get('document_name')
            document_file = request.FILES['document_file'].read()
            base64_file_content = base64.b64encode(document_file).decode('ascii')
            envelope_id = signature_by_email(token, base64_file_content,
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
            return JsonResponse({'docsign_url': '',
                                'envelope_id': '',
                                'message': 'Internal server error (docusign_signature)',
                                'error': str(e)})


@api_view(['GET'])
@csrf_exempt
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
            return JsonResponse({'error': str(error)})


@api_view(['GET'])
@csrf_exempt
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
            return JsonResponse({'msg': str(error)})


@api_view(['GET'])
@csrf_exempt
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
            return JsonResponse({'error': str(error)})


@api_view(['GET'])
@csrf_exempt
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
            return JsonResponse({'error': str(error)})


@api_view(['GET'])
@csrf_exempt
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
            return JsonResponse({'error': str(error)})


@api_view(['GET'])
@csrf_exempt
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
            return JsonResponse({'error': str(error)})


@api_view(['GET'])
@csrf_exempt
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
            return JsonResponse({'error': str(error)})


def docusign_completed(request):
    """Retorna uma resposta quando a assinatura estiver completa."""
    return HttpResponse("Assinatura concluída.")


# ↓ UTIL FUNCTIONS ↓
def signature_by_email(token, base64_file_content,
                       contractor_name, contractor_email,
                       hired_name, hired_email,
                       witness_name, witness_email,
                       document_name):
    """Executa requisição para a API da docusign passando parâmetros de assinantes.
    Cria envelope na plataforma e retorna o ID do envelope.
    
    Args:
    * token: Objeto retornado da API docusign.
    * base64_file_content: Arquivo do documento convertido.
    * contractor_email: E-mail do contratante recebido via POST.
    * contractor_name: Nome do contratante recebido via POST.
    * hired_email: E-mail do contratado recebido via POST.
    * hired_name: Nome do contratado recebido via POST.
    * witness_email: E-mail da testemunha recebido via POST.
    * witness_name: Nome da testemunha recebido via POST.
    * document_name: Nome do documento que será salvo.
    """
    try:
        envelope_args = {'contractor_email': contractor_email,
                         'contractor_name': contractor_name,
                         'hired_email': hired_email,
                         'hired_name': hired_name,
                         'witness_email': witness_email,
                         'witness_name': witness_name,
                         'document_name': document_name,
                         'status': 'sent'}
        envelope_definition = make_envelope(base64_file_content, envelope_args)
        try:
            # Cria e envia o envelope
            api_client = utils.create_api_client('https://demo.docusign.net/restapi', token['access_token'])
            envelope_api = EnvelopesApi(api_client)
            results = envelope_api.create_envelope(account_id=ACCOUNT_ID,
                                                   envelope_definition=envelope_definition)
            envelope_id = results.envelope_id
            return envelope_id
        except Exception as e:
            return JsonResponse({'docsign_url': '',
                                 'envelope id': '',
                                 'message':'Internal server error (Erro ao criar envelope)',
                                 'error': e})
    except Exception as e:
        return JsonResponse({'docsign url': '',
                             'envelope_id': '',
                             'message': 'Internal server error (Erro ao criar objeto)',
                             'error': e})


def make_envelope(base64_file_content, args):
    """Cria a definição de envelope com seu conteúdo. Sendo eles, assinantes,
    testemunhas, documentos e tabs.
    """
    try:
        # Cria uma definição de envelope
        env = EnvelopeDefinition(email_subject='Por favor, assine estes documentos.')
        
        # Cria o objeto documento
        document = Document(document_base64=base64_file_content,
                            name=args['document_name'],
                            file_extension='pdf',
                            document_id='1')
        print(base64_file_content)
        env.documents = [document]
        
        # === ↓ CREATING SIGNERS ↓ ===
        contractor = Signer(email=args['contractor_email'],
                            name=args['contractor_name'],
                            recipient_id='1',
                            routing_order='1')
        hired = Signer(email=args['hired_email'],
                       name=args['hired_name'],
                       recipient_id='2',
                       routing_order='2')
        witness = Signer(email=args['witness_email'],
                         name=args['witness_name'],
                         recipient_id='3',
                         routing_order='3')
        # === ↑ CREATING SIGNERS ↑ ===
        
        # Cria o campo "Assine aqui" (tabs)
        sign_here = SignHere(anchor_string='/sn/',
                             anchor_units='pixels',
                             anchor_y_offset='10',
                             anchor_x_offset='20')
        
        # Adiciona as tabs (sign here) ao assinante 
        contractor.tabs = Tabs(sign_here_tabs=[sign_here])
        hired.tabs = Tabs(sign_here_tabs=[sign_here])
        witness.tabs = Tabs(sign_here_tabs=[sign_here])

        # Adiciona os recipientes no envelope
        recipients = Recipients(signers=[contractor, hired, witness])
        env.recipients = recipients
        
        # Mudar status do envelope
        env.status = args['status']

        return env
    except Exception as e:
        print(f'Erro: {e}')


def create_jwt_grant_token():
    token = utils.docusign_token()
    return token
