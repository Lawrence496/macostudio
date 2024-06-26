# forms.py

from django import forms
from movies.models import Category, Movies

class GenreForm(forms.Form):
    genres = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=True
    )
