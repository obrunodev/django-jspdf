import base64

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    if request.method == 'GET':
        return render(request, 'jspdf/index.html')


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
