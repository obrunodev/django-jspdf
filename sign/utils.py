import jwt
import time

from cryptography.hazmat.primitives import serialization as crypto_serialization
from docusign_esign import ApiClient
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
