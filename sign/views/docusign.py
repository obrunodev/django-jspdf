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


def create_jwt_grant_token():
    token = utils.docusign_token()
    return token


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
            signer_email = request.POST.get('signer_email')
            signer_name = request.POST.get('signer_name')
            cc_email = request.POST.get('cc_email')
            cc_name = request.POST.get('cc_name')
            # document_file = request.POST.get('document_file')
            # print(document_file)
            # signer_type = request.POST.get('type', '')
            with open(os.path.join(BASE_DIR, 'docusign_files/', 'test_file.pdf'), 'rb') as file:
                content_bytes = file.read()
            base64_file_content = base64.b64encode(content_bytes).decode('ascii')
            # if signer_type != 'email':
            #     return JsonResponse({"msg": "Tipo de assinatura inexistente."})
            envelope_id = signature_by_email(token, base64_file_content, signer_email, signer_name, cc_name, cc_email)
            url = ''
            return JsonResponse({'docusign_url': url,
                                 'envelope_id': envelope_id,
                                 'message': 'O envelope foi criado na Docusign',
                                 'error': ''})
            # return JsonResponse({'msg': 'Envelope criado!'})
        except Exception as e:
            return JsonResponse({'docsign_url': '',
                                'envelope_id': '',
                                'message': 'Internal server error (docusign_signature)',
                                'error': str(e)})


def make_envelope(base64_file_content, args):
    """Cria a definição de envelope com seu conteúdo.
    
    - Utiliza um documento PDF para exemplificar.
    """
    # Cria uma definição de envelope
    env = EnvelopeDefinition(email_subject='Por favor, assine estes documentos.')
    
    # Cria o objeto documento
    document = Document(document_base64=base64_file_content,
                        name='Lorem ipsum',
                        file_extension='pdf',
                        document_id='1')
    
    # Insere os documentos no envelope
    env.documents = [document]
    
    # Cria o model recipient do assinante
    # TODO: Receber recipientes para endpoint
    # Signer 1: Contratante
    # Signer 2: Contratado
    # Signer 3: Testemunha
    signer = Signer(email=args['signer_email'],
                    name=args['signer_name'],
                    recipient_id='1',
                    routing_order='1')
    
    # Cria um objeto cc que receberá a cópia dos documentos
    cc = CarbonCopy(email=args['cc_email'],
                    name=args['cc_name'],
                    recipient_id='2',
                    routing_order='2')
    
    # Cria o campo "Assine aqui" (tabs)
    sign_here = SignHere(anchor_string='/sn/',
                         anchor_units='pixels',
                         anchor_y_offset='10',
                         anchor_x_offset='20')
    
    # Adiciona as tabs (sign here) ao assinante 
    signer.tabs = Tabs(sign_here_tabs=[sign_here])
    
    # Adiciona os recipientes no envelope
    recipients = Recipients(signers=[signer], carbon_copies=[cc])
    env.recipients = recipients
    
    # Mudar status do envelope
    env.status = args['status']
    
    return env


def signature_by_email(token, base64_file_content, signer_email, signer_name, cc_name, cc_email):
    try:
        envelope_args = {'signer_email': signer_email,
                         'signer_name': signer_name,
                         'cc_email': cc_email,
                         'cc_name': cc_name,
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


def docusign_completed(request):
    """Retorna uma resposta quando a assinatura estiver completa."""
    return HttpResponse("Assinatura concluída.")


@api_view(['GET'])
@csrf_exempt
def get_envelope_status(request, envelope_id):
    token = create_jwt_grant_token()
    post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
    base_url = 'https://account-d.docusign.com/oauth/token'
    r = requests.post(base_url, data=post_data)
    token = r.json()
    base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}'
    r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
    response = r.json()
    return JsonResponse(response)


@api_view(['GET'])
@csrf_exempt
def envelopes_list(request):
    """Lista todos os envelopes cadastrados no docusign."""
    token = create_jwt_grant_token()
    post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
    base_url = 'https://account-d.docusign.com/oauth/token'
    r = requests.post(base_url, data=post_data)
    token = r.json()
    # base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/search_folders/awaiting_my_signature'
    base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/search_folders/all'
    r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
    response = r.json()
    return JsonResponse(response)


@api_view(['GET'])
@csrf_exempt
def envelope_documents(request, envelope_id):
    """Lista os documentos de um envelope."""
    if request.method == 'GET':
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


@api_view(['GET'])
@csrf_exempt
def download_documents(request, envelope_id, document_id):
    """Baixa os documentos de um envelope."""
    if request.method == 'GET':
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
        # temp_file contém o caminho do arquivo na pasta temp
        # return FileResponse(temp_file)  retorna o caminho
        file = open(temp_file, "rb")
        return FileResponse(file, as_attachment=True)  # Faz download do arquivo.
    
    
@api_view(['GET'])
@csrf_exempt
def download_all_documents(request, envelope_id):
    """Baixa os documentos de um envelope."""
    if request.method == 'GET':
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
        # temp_file contém o caminho do arquivo na pasta temp
        # return FileResponse(temp_file)  retorna o caminho
        file = open(temp_file, "rb")
        return FileResponse(file, as_attachment=True)  # Faz download do arquivo.
