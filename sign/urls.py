from django.urls import path, re_path

from sign.views import remote_sign
from sign import docusign

app_name = 'sign'
urlpatterns = [
    path('', remote_sign.index, name='index'),
    path('make_envelope/', remote_sign.make_envelope, name='make_envelope'),
    path('get_envelope_status/<str:envelope_id>', docusign.get_envelope_status, name='get_envelope_status'),
    path('envelopes_list/', docusign.envelopes_list, name='envelopes_list'),
    path('docusign_signature/', docusign.docusign_signature, name='docusign_signature'),
    # re_path(r'^docusign_signature/$', docusign.docusign_signature, name='docusign_signature'),
    re_path(r'^sign_completed/$', docusign.docusign_completed, name='docusign_completed'),
]
