from django import forms
from django.forms import ModelForm

class EmailForm(forms.Form):
    name = forms.CharField(max_length=40)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget = forms.Textarea)

class EmailPostForm(ModelForm):
    pass
