# Integração Docusign

Ferramenta que visa facilitar a integração de outras plataformas com a Docusign.

## Rotas disponíveis

Endpoints disponíveis para consumo.

Gera um envelope na docusign com assinantes e documento. (Envia e-mails em seguida)
```
POST /sign/docusign_signature/
```
Body:
```json
{
    "contractor_email": "contractor@example.com",
    "contractor_name": "Contractor Example",
    "hired_email": "hired@example.com",
    "hired_name": "Hired Example",
    "witness_email": "witness@example.com",
    "witness_name": "Witness Example",
    "document_name": "Uploaded document name"
}
```

Retorna lista de envelopes:
```
GET /sign/envelopes_list/
```

Retorna detalhes de um envelope:
```
GET /sign/get_envelope_status/{envelope_id}
```

Retorna recipientes de um envelope:
```
GET /sign/envelopes/{envelope_id}/recipients/
```

Lista de documentos em um envelope:
```
GET /sign/envelopes/{envelope_id}/documents/
```

Faz download de um documento:
```
GET /sign/envelopes/{envelope_id}/documents/{document_id}/download/
```

Faz download de todos os documentos do envelope:
```
GET /sign/envelopes/{envelope_id}/documents/download/
```

Rota de feedback do usuário usuário:
```
GET /sign/docusign_completed/
```
