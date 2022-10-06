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
    print('TOKEN GERADO:', token)
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
            print(signer_type)
            # url, envelope_id = signature_by_embedded(token, base64_file_content, signer_name, signer_email)
        elif signer_type == 'email':
            envelope_id = signature_by_email(token, base64_file_content, signer_name, signer_email)
            url = ''
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


def signature_by_email(token, base64_file_content, signer_name, signer_email):
    try:
        document = Document( # Cria um objeto do documento
            document_base64 = base64_file_content,
            name = 'Example document', # Não precisa ter mesmo nome do arquivo
            file_extension = 'pdf', # Aceita pdf, docx...
            document_id = '1' # Referência do documento
        )
        sign_here = SignHere(document_id = '1',
                             page_number = '1',
                             recipient_id= '1',
                             tab_label = 'SignHereTab',
                             y_position='513',
                             x_position='80')
        today = date.today()
        curr_date = today.strftime('%d/%m/%Y')
        sign_date = DateSigned(document_id = '1',
                               page_number = '1',
                               recipient_id= '1',
                               tab_label = 'Date',
                               font='helvetica',
                               bold='true',
                               value=curr_date,
                               tab_id='date',
                               font_size='size16',
                               y_position='55',
                               x_position='650')
        text_name = Text(document_id = '1',
                         page_number = '1',
                         recipient_id= '1',
                         tab_label = 'Name',
                         font='helvetica',
                         bold='true',
                         value=signer_name,
                         tab_id='name',
                         font_size='size16',
                         y_position='280',
                         x_position='54')
        text_email = Text(document_id = '1',
                          page_number = '1',
                          recipient_id= '1',
                          tab_label = 'Email',
                          font='helvetica',
                          bold='true',
                          value=signer_email,
                          tab_id='email',
                          font_size='size16',
                          y_position='304',
                          x_position='82')
        signer_tab = Tabs(sign_here_tabs=[sign_here], text_tabs=[text_name, text_email, sign_date])
        signer = Signer(email=signer_email, name=signer_name, recipient_id='1', routing_order='1', tabs=signer_tab)
        # Cria uma cópia e envia o documento para o mesmo.
        cc1 = CarbonCopy(email=signer_email,
                         name=signer_name,
                         recipient_id='2',
                         routing_order='2')
        # Criar um objeto envelope e popular com as informações acima.
        envelope_definition = EnvelopeDefinition(
            email_subject = 'Please sign this document sent from the Python SDK',
            documents = [document], # The Recipients object wants arrays for each recipient type
            recipients = Recipients(signers=[signer], carbon_copies=[cc1]),
            status = 'sent' # requests that the envelope be created and sent.
        )
        try:
            # Cria e envia o envelope
            api_client = ApiClient()
            api_client.host = 'https://demo.docusign.net/restapi',
            api_client.set_default_header('Authorization', 'Bearer ' + token['access token'])
            envelope_api = EnvelopesApi(api_client),
            results = envelope_api.create_envelope(account_id=ACCOUNT_ID,
                                                   envelope_definition=envelope_definition)
            envelope_id = results.envelope_id
            return envelope_id
        except Exception as e:
            return JsonResponse({'docsign_url': '',
                                 'envelope id': '',
                                 'message':'Internal server error (Erro ao criar envelope)',
                                 'error': str(e)})
    except Exception as e:
        return JsonResponse({'docsign url': '',
                             'envelope_id': '',
                             'message': 'Internal server error (Erro ao criar objeto)',
                             'error': str(e)})


def docusign_completed(request):
    """Retorna uma resposta quando a assinatura estiver completa."""
    return HttpResponse("Assinatura concluída.")
