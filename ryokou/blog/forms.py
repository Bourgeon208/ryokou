from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Conversation, Message


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': "Nom d'utilisateur"})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirmer le mot de passe'})
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input comment-textarea',
                'placeholder': 'Votre commentaire...',
                'rows': 4,
            }),
        }
        labels = {'content': ''}


class NewConversationForm(forms.ModelForm):
    first_message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Votre message...',
            'rows': 6,
        })
    )

    class Meta:
        model = Conversation
        fields = ['subject']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Sujet de votre message',
            }),
        }
        labels = {'subject': 'Sujet'}


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input reply-textarea',
                'placeholder': 'Votre réponse...',
                'rows': 3,
            }),
        }
        labels = {'content': ''}
