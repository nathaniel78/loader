import os
import logging
import socket
import paramiko
import tempfile
from scp import SCPClient
from django.views import View
from .models import Host, Command
from django.contrib import messages
from .utils import hash_person, pagination_utils
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (
    HostForm, 
    CommandForm
)

logger = logging.getLogger(__name__)


# View para upload
class UploadView(View):
    def get(self, request):
        hosts = Host.objects.all()
        commands = Command.objects.all()
        context = {
            'hosts': hosts,
            'commands': commands,
        }
        
        return render(request, 'pages/upload.html', context)


# View home upload
class UploadActionView(View):
    def post(self, request, host_id, command_id):
        command = get_object_or_404(Command, id=command_id)
        host = get_object_or_404(Host, id=host_id)
        uploaded_file = request.FILES.get("file")
        
        hosts = Host.objects.all()
        commands = Command.objects.all()
        
        if not uploaded_file:
            messages.add_message(request, constants.ERROR, "Nenhum arquivo foi enviado.")
            return redirect('home')
        
        password_decrypt = hash_person.PasswordFernetKey.return_hash(host.id)
        print(f"Senha descriptografada: {password_decrypt}")

        # Configurações do Host
        ip = host.host_ip
        username = host.host_user
        password = password_decrypt
        remote_dir = host.host_dir

        # Salva o arquivo temporariamente e obtém o nome original
        original_filename = uploaded_file.name
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name 

        stdout_before = ""
        stderr_before = ""
        stdout_after = ""
        stderr_after = ""

        pre_upload_message = "Comando pré-upload não executado."
        post_upload_message = "Comando pós-upload não executado."

        try:
            # Conexão SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)

            # Define um tempo limite (em segundos)
            command_timeout = 120

            # Executa o comando antes do upload, se houver
            if command.command_before:
                stdin, stdout, stderr = ssh.exec_command(command.command_before, timeout=command_timeout)
                stdout_before = stdout.read().decode()
                stderr_before = stderr.read().decode()
                if stderr_before:
                    pre_upload_message = f"Erro no comando pré-upload: {stderr_before}"
                else:
                    pre_upload_message = "Comando pré-upload executado com sucesso."

            # Envia o arquivo via SCP com o nome original
            with SCPClient(ssh.get_transport()) as scp:
                scp.put(temp_file_path, remote_path=f"{remote_dir}/{original_filename}")

            logger.info(f"Arquivo {temp_file_path} enviado com sucesso para {remote_dir} em {ip} com o nome {original_filename}.")

            # Executa o comando após o upload, se houver
            if command.command_after:
                stdin, stdout, stderr = ssh.exec_command(command.command_after, timeout=command_timeout)
                stdout_after = stdout.read().decode()
                stderr_after = stderr.read().decode()
                if stderr_after:
                    post_upload_message = f"Erro no comando pós-upload: {stderr_after}"
                else:
                    post_upload_message = "Comando pós-upload executado com sucesso."

            messages.add_message(request, constants.SUCCESS, "Arquivo enviado com sucesso.")
        
        except socket.timeout:
            messages.add_message(request, constants.ERROR, "O comando excedeu o tempo limite de execução.")
            logger.error("O comando excedeu o tempo limite de execução.")
        
        except Exception as e:
            messages.add_message(request, constants.ERROR, f"Ocorreu um erro: {e}.")
            logger.error(f"Ocorreu um erro ao conectar e enviar o arquivo: {e}")
        
        finally:
            ssh.close()
            os.remove(temp_file_path)

        context = {
            'stdout_before': stdout_before,
            'stderr_before': stderr_before,
            'stdout_after': stdout_after,
            'stderr_after': stderr_after,
            'pre_upload_message': pre_upload_message,
            'post_upload_message': post_upload_message,
            'hosts': hosts,
            'commands': commands,
        }
        context.update()
        
        return render(request, 'pages/upload.html', context)
    
 
# View command
class CommandView(View):
    def get(self, request):
        lista = Command.objects.all()
        commands = pagination_utils.Pagination.pg_default(request, lista, 10)
        context = {
            'commands': commands,
        }
        
        return render(request, 'pages/command.html', context)
    

# View command create
class CommandCreateView(View):
    def get(self, request):
        commands = Command.objects.all()
        form = CommandForm()
        context = {
            'form': form,
        }
        return render(request, 'pages/command_form.html', context)

    def post(self, request):
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save(commit=False)
            command.save()
            messages.add_message(request, constants.SUCCESS, 
                                     'Cadastro realizado com sucesso.')
            return redirect('command_list')
            
        return render(request, 'pages/command_form.html')


# View Command update
class CommandUpdateView(View):
    def get(self, request, id):
        instancia = get_object_or_404(Command, id=id)
        form = CommandForm(instance=instancia)
        context = {
            'form': form,
            'instancia': instancia
        }
        return render(request, 'pages/command_form.html', context)


    def post(self, request, id):
        Command_instance = get_object_or_404(Command, id=id)
        form = CommandForm(request.POST, instance=Command_instance)

        if form.is_valid():
            command = form.save(commit=False)
            command.name = form.cleaned_data["name"]
            command.description = form.cleaned_data["description"]
            command.command_before = form.cleaned_data["command_before"]
            command.command_after = form.cleaned_data["command_after"]

            command.save()
            
            messages.add_message(request, constants.SUCCESS, 
                                     'Atualização realizada com sucesso.')
            return redirect('command_list')
        
        return render(request, 'pages/command_form.html', {'form': form})


# View command delete
class CommandDeleteView(View):
    def get(self, request, id):
        command = get_object_or_404(Command, id=id)
        
        if command:
            command.delete()
            messages.add_message(request, constants.SUCCESS, 
                                     'Exclusão realizada com sucesso.')
            return redirect('command_list') 


# View host
class HostView(View):
    def get(self, request):
        lista = Host.objects.all()
        hosts = pagination_utils.Pagination.pg_default(request, lista, 10)
        context = {
            'hosts': hosts,
        }
        
        return render(request, 'pages/host.html', context)


# View host create
class HostCreateView(View):
    def get(self, request):
        form = HostForm()
        context = {
            'form': form,
        }
        return render(request, 'pages/host_form.html', context)

    def post(self, request):
        form = HostForm(request.POST)
        if form.is_valid():
            host = form.save(commit=False)
            host.host_password = hash_person.PasswordFernetKey.make_hash(form.cleaned_data["host_password"])
            host.save()
            messages.add_message(request, constants.SUCCESS, 
                                     'Cadastro realizado com sucesso.')
            return redirect('host_list')
        return render(request, 'pages/host_form.html', {'form': form})
    

# View host update
class HostUpdateView(View):
    def get(self, request, id):
        instancia = get_object_or_404(Host, id=id)
        form = HostForm(instance=instancia)

        return render(request, 'pages/host_form.html', {'form': form, 'instancia': instancia})


    def post(self, request, id):
        host_instance = get_object_or_404(Host, id=id)
        form = HostForm(request.POST, instance=host_instance)        

        if form.is_valid():
            host = form.save(commit=False)
            host.host_ip = form.cleaned_data["host_ip"]
            host.host_user = form.cleaned_data["host_user"]
            host.host_dir = form.cleaned_data["host_dir"]

            password_old = request.POST.get("host_password")
            print("Senha antiga:", password_old)
            
            password_new = request.POST.get("password", "").strip()
            print("Senha nova:", password_new)

            if password_new == '' or password_new == None:
                host.host_password = password_old
                
            else:
                host.host_password = hash_person.PasswordFernetKey.make_hash(password_new)

            host.save()
            
            messages.add_message(request, constants.SUCCESS, 
                                     'Atualização realizada com sucesso.')
            return redirect('host_list')
        
        return render(request, 'pages/host_form.html', {'form': form})


# View host delete
class HostDeleteView(View):
    def get(self, request, id):
        host = get_object_or_404(Host, id=id)
        
        if host:
            host.delete()
            messages.add_message(request, constants.SUCCESS, 
                                     'Exclusão realizada com sucesso.')
            return redirect('host_list') 

