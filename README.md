# Integração Docusign

Ferramenta que visa facilitar a integração de outras plataformas com a Docusign.

## Rotas disponíveis

Endpoints disponíveis para consumo.

```
GET /sign/envelopes_list/ - Retorna lista de envelopes.
GET /sign/get_envelope_status/{envelope_id} - Retorna detalhes de um envelope.
GET /sign/docusign_completed/ - Rota usada para retornar um feedback ao usuário.
GET /sign/envelopes/{envelope_id}/documents/ - Lista documentos de um envelope.
GET /sign/envelopes/{envelope_id}/documents/{document_id}/download/ - Faz download de um documento.

POST /sign/docusign_signature/ - Cria um envelope com dados passados e dispara e-mails para os "signers".
```
