from django import forms
from django.core.validators import FileExtensionValidator, ValidationError
from .models import Host, Command


class FileValidatorForm(forms.Form):
    file = forms.FileField(
        label="Arquivo",
        validators=[
            FileExtensionValidator(['zip']),  # Valida extensão do arquivo
        ]
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        max_size = 100 * 1024 * 1024  # Limite de 100 MB

        if file.size > max_size:
            raise ValidationError("O arquivo não pode exceder 100 MB.")

        return file
    


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host_ip', 'host_user', 'host_password', 'host_dir']



class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['name', 'description', 'command_before', 'command_after']