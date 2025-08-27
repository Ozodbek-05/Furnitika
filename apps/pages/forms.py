from django import forms


class ContactForms(forms.Form):
    full_name = forms.CharField(max_length=128)
    email = forms.EmailField(unique=True)
    subject = forms.CharField(max_length=128, required=False)
    message = forms.Textarea()

    def clean(self):
        print("1. object level validation")
        print(self.cleaned_data)
        return super().clean()


