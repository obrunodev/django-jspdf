import time

from cryptography.hazmat.primitives import serialization as crypto_serialization
from django.http import JsonResponse
from docusign_esign import (RecipientViewRequest, EnvelopeDefinition, Document,
                            Signer, SignHere, Tabs, Recipients, ApiClient,
                            EnvelopesApi, Text, DateSigned, CarbonCopy, Envelope)
from jose import jws
from project import settings

def docusign_token():
    """Função que retorna o token de autenticação com tempo de expiração de 24 horas."""
    iat = time.time()
    exp = iat+(3600*24)
    payload = {"sub": settings.CLIENT_USER_ID,
               "iss": settings.CLIENT_AUTH_ID,
               "iat": iat, # Início de "vida" do token
               "exp": exp, # Momento da expiração do token (3600*24 == 1 dia)
               "aud": "account-d.docusign.com",
               "scope": "signature"}
    with open('private.key', "rb") as key_file:
        private_key = crypto_serialization.load_pem_private_key(key_file.read(), password=None)
    key = private_key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8, crypto_serialization.NoEncryption())
    jwt_token = jws.sign(payload, key, algorithm='RS256')
    return jwt_token


def create_api_client(base_path, access_token):
    """Create api client and construct API headers"""
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {access_token}")

    return api_client


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
            api_client = create_api_client('https://demo.docusign.net/restapi', token['access_token'])
            envelope_api = EnvelopesApi(api_client)
            results = envelope_api.create_envelope(account_id=settings.ACCOUNT_ID,
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
                             'error': e})


def make_envelope(base64_file_content, args):
    """Cria a definição de envelope com seu conteúdo. Sendo eles, assinantes,
    testemunhas, documentos e tabs.
    """
    try:
        # Cria uma definição de envelope
        env = EnvelopeDefinition(email_subject='Por favor, assine estes documentos.',
                                 email_blurb='Assine o documento clicanco no link acima.')
        
        # Cria o objeto documento
        document = Document(document_base64=base64_file_content,
                            name=args['document_name'],
                            file_extension='pdf',
                            document_id='1')
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
