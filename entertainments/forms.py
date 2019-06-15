from django import forms
from.models import CommunityContent

class UploadForm(forms.ModelForm):
    class Meta:
        model = CommunityContent
        fields = ['title', 'thumbnail','video']
