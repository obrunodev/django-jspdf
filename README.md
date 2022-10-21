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
    "parameter": "argument"
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
Body:
```json
{
    "parameter": "argument"
}
```


```
GET /sign/docusign_completed/ - Rota usada para retornar um feedback ao usuário.

 - Cria um envelope com dados passados e dispara e-mails para os "signers".
```
