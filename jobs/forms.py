from django import forms
from .models import Response


class SearchForm(forms.Form):
    query = forms.CharField()



class ResumePostForm(forms.Form):
    class Meta:
        model = Request
        fields = ['firstname', 'surname', 'lastname', 'e_mail', 'phone', 'text', 'job', 'cv' ]