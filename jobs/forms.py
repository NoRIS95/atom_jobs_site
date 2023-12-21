from django import forms


class SearchForm(forms.Form):
    query = forms.CharField()

# class ResumePostForm(forms.Form):
#     name = forms.CharField(max_length=25)
#     surname = forms.CharField(max_length=40)
#     email = forms.EmailField()
#     resume_file = models.FileField(upload_to='cv/')
#     comments = forms.CharField(required=False,
#                                widget=forms.Textarea)