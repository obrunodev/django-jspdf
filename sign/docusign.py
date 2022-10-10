import base64
import requests
import os
import json
import jwt

from datetime import date
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from docusign_esign import (RecipientViewRequest, EnvelopeDefinition, Document,
                            Signer, SignHere, Tabs, Recipients, ApiClient,
                            EnvelopesApi, Text, DateSigned, CarbonCopy)
from project.settings import ACCOUNT_ID, BASE_DIR, CLIENT_AUTH_ID, CLIENT_USER_ID
# from rest_framework.decorators import api_view
from sign import tokens


def create_jwt_grant_token():
    token = tokens.docusign_token()
    # print('TOKEN GERADO:', token)
    return token


@csrf_exempt
def docusign_signature(request):
    try:
        token = create_jwt_grant_token()
        post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                     'assertion': token}
        base_url = 'https://account-d.docusign.com/oauth/token'
        r = requests.post(base_url, data=post_data)
        token = r.json()
        data = json.loads(request.body)
        signer_email = data['email']
        signer_name = data['full_name']
        signer_type = data['type']
        with open(os.path.join(BASE_DIR, 'docusign_files/', 'test_file.pdf'), 'rb') as file:
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode('ascii')
        if signer_type == 'embedded':
            url = ''
            envelope_id = ''
            # url, envelope_id = signature_by_embedded(token, base64_file_content, signer_name, signer_email)
        elif signer_type == 'email':
            envelope_id = signature_by_email(token, base64_file_content, signer_name, signer_email)
            url = ''
        print('Chegou aqui: docusign.py, linha 47.')
        # return JsonResponse({'docusign_url': url,
        #                      'envelope_id': envelope_id,
        #                      'message': 'Docusign',
        #                      'error': ''})
        return HttpResponse('Deu certo')
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


def signature_by_email(token, base64_file_content):
    try:
        envelope_args = {'signer_email': 'bruno.pianca@alstratech.com',
                         'signer_name': 'Bruno',
                         'cc_email': 'brunorpdev@gmail.com',
                         'cc_name': 'Bruno',
                         'status': 'sent'}
        envelope_definition = make_envelope(base64_file_content, envelope_args)
        try:
            # Cria e envia o envelope
            api_client = ApiClient()
            api_client.host = 'https://demo.docusign.net/restapi'
            api_client.set_default_header('Authorization', 'Bearer ' + token['access_token'])
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


def get_envelope_status(request, envelope_id):
    token = create_jwt_grant_token()
    post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
    base_url = 'https://account-d.docusign.com/oauth/token'
    r = requests.post(base_url, data=post_data)
    token = r.json()
    base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}'
    r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
    response = r.json()
    return HttpResponse(str(response))


def envelopes_list(request):
    """Lista todos os envelopes cadastrados no docusign."""
    token = create_jwt_grant_token()
    post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
    base_url = 'https://account-d.docusign.com/oauth/token'
    r = requests.post(base_url, data=post_data)
    token = r.json()
    base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{ACCOUNT_ID}/search_folders/awaiting_my_signature'
    r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
    response = r.json()
    return HttpResponse(str(response))
