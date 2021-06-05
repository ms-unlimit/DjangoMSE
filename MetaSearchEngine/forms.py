from django import forms
from .models import Query

class QueryForm(forms.ModelForm):
    class Meta:
        model= Query
        fields = ['query']
        # labels = {'query':'query_lable'}
        # widgets ={'query': forms.Textarea(attrs={'cols':80})}