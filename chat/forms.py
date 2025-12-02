from django import forms
from django.forms import ModelForm
from .models import GroupMessage

class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'rows': 1,
                'placeholder': 'Type a message...',
                'class': 'w-full bg-gray-100 text-black text-sm p-2 focus:outline-none resize-none',
                'maxlength': '500',
                'autofocus': True,
            }),
        }
