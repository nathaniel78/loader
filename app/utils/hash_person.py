from django.conf import settings
from cryptography.fernet import Fernet
from ..models import Host
from django.core.exceptions import ObjectDoesNotExist



'''
Info: Chave Fernet fixa que deve ser gerada e registrada em FERNET_KEY, depois comentado o trecho abaixo
não ficar gerando novas key
Url: https://cryptography.io/en/latest/fernet/#cryptography.fernet.Fernet
'''
# key = Fernet.generate_key()
# print('---------------------> ' + key.decode() + ' <--------------------------')
FERNET_KEY = 'OBxRpHZU1pLTf0vsXrMK0eA1YwEPgC3MeQqCMSs9XCE='
cipher_suite = Fernet(FERNET_KEY)

class PasswordFernetKey:
    
    @staticmethod
    def make_hash(password):
        try:
            # Criptografa a senha e retorna como string Base64
            pwd_hash = cipher_suite.encrypt(password.encode())
            return pwd_hash.decode()
        except Exception as e:
            print(f"Erro ao criptografar: {e}")
            return str(e)
    
    @staticmethod
    def return_hash(id):
        try:
            host = Host.objects.get(id=id)
            pwd_after = host.host_password
            print('id ->', id)
            print(f"Senha criptografada recuperada do banco: {pwd_after}")

            # Descriptografa a senha
            pwd_before = cipher_suite.decrypt(pwd_after.encode()).decode('utf-8')
            print(f"Senha descriptografada: {pwd_before}")
            return pwd_before
            
        except ObjectDoesNotExist:
            print("Host não encontrado.")
            return None
            
        except Exception as e:
            print(f"Erro na descriptografia: {e}")
            return None
