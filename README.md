# Django with jsPDF

Projeto para gerar arquivos PDF diretamente no frontend, permitindo que o mesmo seja enviado via e-mail através da ferramenta de e-mails do Django.

---

## Requisitos

- Necessário ter Django 3.2 instalado:

```
pip install django==3.2.*
```

- Necessário algumas libs JS para funcionar:
    - jquery
    - jspdf
    - dompurify
    - html2canvas

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.3/jquery.min.js" integrity="sha512-STof4xm1wgkfm7heWqFJVn58Hm3EtS31XFaagaa8VMReCXAkQnJZ+jEy8PCC/iT18dFy95WcExNHFTqLyp72eQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/2.4.1/purify.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
```

---

## Como funciona?

Primeiro é necessário configurar o jsPDF para a janela aberta no navegador:

```javascript
window.jsPDF = window.jspdf.jsPDF;
```

Em seguida será necessário ter um código HTML que o jsPDF usará para gerar o documento, este código pode estar dentro de uma string ou até mesmo ser refereciado um elemento na página atual.
Nesse caso será usado uma string com o seguinte código:

```javascript
var document_content = `
    <div class="aqua-square"></div>

    <img src="{% static 'img/teste.jpg' %}" height="150px" width="150px" alt="">

    <h1 class="title">Documento PDF (h1)</h1>
    <h2 class="title">Documento PDF (h2)</h2>
    <h3 class="title">Documento PDF (h3)</h3>

    <p>Este documento pode receber um corpo com tags HTML. (p)</p>

    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>

    <ol>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ol>
`
```

Como pode ver, alguns elementos possuem classes, sendo assim, é possível customizar as classes dentro do próprio aquivo HTML que esses elementos herdarão o estilo.
No caso, temos duas classes: aqua-square e title:

```css
.aqua-square {
    background: aqua;
    height: 150px;
    width: 150px;
}
.title { color: red; }
```

Agora vamos usar os elementos acima para contruir o nosso PDF, usando o código javascript a seguir:

```javascript
function enviarPDF() {
    const doc = new jsPDF();
    doc.html(document_content, {
        callback: function(doc) {
            const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            let obj = doc.output('datauristring');
            $.ajax({
                url: "{% url 'jspdf:send_pdf' %}",
                data: {
                    'file': obj,
                    'csrfmiddlewaretoken': csrftoken
                },
                method: "post",
                success: function(response) { console.log('Finalizado') }
            });
        },
        x: 15,
        y: 15,
        width: 170,
        windowWidth: 650
    });
}
```

**Explicando o código:**

- Primeiro instanciamos o objeto jsPDF em uma variável.
- Depois chamamos o método html, passando como primeiro parâmetro o trecho html que queremos inserir no documento.
- Em seguida temos as options, que terá um callback, executando assim que o documento é montado.
- Na callback, basta pegarmos o código csrf gerado pelo Django e o resultado do método output do jsPDF.
    - O argumento do output define o "formato" que tal informação será recebido.
- Agora basta enviar uma requisição POST via AJAX para uma URL do Django, passando os parâmetros do obj e do csrftoken.

**Agora o código Python**

Aqui vamos considerar que já exista uma view configurada para receber essa requisição.
Sendo assim, temos a seguinte função:

```python
import base64

from django.core.mail import EmailMessage
from django.http import HttpResponse

def send_pdf(request):
    if request.method == 'POST':
        try:
            pdf_output = request.POST.get('file', '')
            pdf_output = base64.b64decode(pdf_output.split(',')[-1])
            email = EmailMessage(
                subject='Assunto aqui',
                body='Corpo do e-mail',
                from_email='email.origem@email.com',
                to=['email.destino@email.com'],
            )
            email.attach('file.pdf', pdf_output, 'application/pdf')
            result = email.send(fail_silently=False)
        except Exception as e:
            raise e
        
    return HttpResponse(f'E-mail enviado: {result}.', status=200)
```

**Explicando o código**

- Pegamos o data da requisição, mais especificamente o valor de "file", e instanciamos o mesmo em uma variável.
- Fazemos um split na string, pegando somente o último objeto, sendo o único trecho referente ao conteúdo do PDF encriptado.
    - O resultado disso nós decriptamos através da lib built-in base64 do python.
- Agora basta criar um objeto de e-mail do próprio Django (EmailMessage), e adicionar o arquivo ao objeto através do método attach.
- Por fim, chamamos o método send() para enviar o e-mail.
