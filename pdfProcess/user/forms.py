from django import forms
from .models import PdfLoad

class PdfLoadForm(forms.ModelForm):
    class Meta:
        model = PdfLoad
        fields = ["createdPdf"]