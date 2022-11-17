from django import forms

from perguntas.models import Pergunta, Resposta


class PerguntaForm(forms.ModelForm):
    
    class Meta:
        model = Pergunta
        fields = ['nome', 'pergunta']


class RespostaForm(forms.ModelForm):
    
    class Meta:
        model = Resposta
        fields = ['nome', 'resposta']
