from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Host, Command


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    ) 


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host_ip', 'host_user', 'host_password', 'host_dir']



class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['name', 'description', 'command_before', 'command_after']