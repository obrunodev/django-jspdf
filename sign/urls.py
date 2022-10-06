from django.urls import path, re_path

from sign.views import remote_sign
from sign import docusign

app_name = 'sign'
urlpatterns = [
    path('', remote_sign.index, name='index'),
    path('test_return/', remote_sign.test_return, name='test_return'),
    re_path(r'^docusign_signature/$', docusign.docusign_signature, name='docusign_signature'),
    re_path(r'^sign_completed/$', docusign.docusign_completed, name='docusign_completed'),
]
