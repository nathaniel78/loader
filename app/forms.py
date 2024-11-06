from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Host, Command


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host_ip', 'host_user', 'host_password', 'host_dir']


class CommandForm(forms.ModelForm):
    class Meta:
        model = Command
        fields = ['name', 'description', 'command_before', 'command_after']