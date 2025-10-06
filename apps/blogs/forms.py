from django import forms
from .models import BlogCommentModel

class ContactForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['name', 'email', 'website', 'message']