from django.urls import path, re_path

from sign.views import general
from sign.views import docusign

app_name = 'sign'
urlpatterns = [
    path('', general.index, name='index'),
    path('make_envelope/', general.make_envelope, name='make_envelope'),
    
    path('get_envelope_status/<str:envelope_id>', docusign.get_envelope_status, name='get_envelope_status'),
    path('envelopes_list/', docusign.envelopes_list, name='envelopes_list'),
    path('docusign_signature/', docusign.docusign_signature, name='docusign_signature'),
    path('sign_completed/', docusign.docusign_completed, name='docusign_completed'),
    path('envelopes/<str:envelope_id>/documents/', docusign.envelope_documents, name='envelope_documents'),
    path('envelopes/<str:envelope_id>/documents/<str:document_id>/download/', docusign.download_documents, name='download_documents'),
    path('envelopes/<str:envelope_id>/documents/download/', docusign.download_all_documents, name='download_all_documents'),
    # re_path(r'^docusign_signature/$', docusign.docusign_signature, name='docusign_signature'),
    # re_path(r'^sign_completed/$', docusign.docusign_completed, name='docusign_completed'),
]
