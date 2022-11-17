from django.db import models


class Pergunta(models.Model):
    nome = models.CharField(max_length=255)
    pergunta = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s perguntou "%s"' % (self.nome, self.pergunta)
