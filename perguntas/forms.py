from django import forms

from perguntas.models import Pergunta, Resposta


class PerguntaForm(forms.ModelForm):
    
    class Meta:
        model = Pergunta
        fields = ['nome', 'titulo', 'descricao']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control',
                                                 'placeholder': 'Digite seu nome'})
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})


class RespostaForm(forms.ModelForm):
    
    class Meta:
        model = Resposta
        fields = ['nome', 'resposta']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control',
                                                 'placeholder': 'Digite seu nome'})
        self.fields['resposta'].widget.attrs.update({'class': 'form-control'})
