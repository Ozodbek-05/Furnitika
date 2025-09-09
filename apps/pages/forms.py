from django import forms
from apps.pages.models import ContactModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        exclude = ['is_read', 'comment']


    def clean(self):
        print(self.cleaned_data)
        return super().clean()

    def clean_email(self):
        email: str = self.cleaned_data.get('email')
        if not email.endswith(".com"):
            raise forms.ValidationError("Email must end with .com")
        return self.cleaned_data.get('email')