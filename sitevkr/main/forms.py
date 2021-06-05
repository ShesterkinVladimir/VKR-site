from django import forms
from .models import UploadedFile

#DataFlair #File_Upload
class Upload_Form(forms.ModelForm):

    class Meta:
        model = UploadedFile
        fields = [
            'file'
        ]
