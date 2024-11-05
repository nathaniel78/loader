from django.db import models


'''
Name: class host
Description: responsável pelas informações do host
'''
class Host(models.Model):
    host_ip = models.GenericIPAddressField(blank=False, null=False)
    host_user = models.CharField(max_length=50, blank=False, null=False)
    host_password = models.CharField(max_length=200, blank=True, null=True)
    host_dir = models.CharField(max_length=255, blank=False, null=False)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.host_ip} - {self.host_user}"

'''
Name: class command
Description: responsável pelos comandos
'''
class Command(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    command_before = models.TextField(blank=True, null=True)
    command_after = models.TextField(blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
