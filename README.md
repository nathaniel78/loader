## Uso do Código:
Este código está disponível para uso com restrições comerciais e requer autorização para modificações.

- **Uso Pessoal e Não Comercial**: Permitido sem a necessidade de autorização.
- **Modificações e Uso Comercial**: Proibidos sem autorização prévia. Para modificações ou uso comercial, entre em contato com [nathanieljose78@gmail.com] para obter permissão.

## Sobre:
```
Loader é um aplicativo para realizar ações pós e após o upload do arquivo que aceita tando senha como sem e certificado para conexão ssh.
```

## Instalar:
```
1 - Depois de baixar o projeto, copie para raiz o docker/.env.exemple como .env e coloque os valores.
2 - Executar o comando docker-compose up -d --build
3 - Criar um usuário com o comando docker exec -it loader python manage.py createsuperuser
4 - Campos obrigatório, usuário e password.
5 - Caso necessite resetar a senha docker exec -it loader python manage.py changepassword seu_usuario
6 - Demais comandos docker exec -it loader python manage.py --help

Obs: no docker-compose o trecho que está com o comentário sobre o volume do certs, ele deve ser comentado, baso a aplicação
esteja rodando direto no host, nesse caso deve ser comentado esse volume, caso esteja rodando em docker, container, deve
passar os valores, PATH_CERTS e NAME_CERTS, sendo o caminho absoluto do certificado no host e o nome do arquivo, exemplo,
/root/.certs e certs.pem. Lembre-se que o arquivo deve ser dado a permissão apenas de leitura, questão de segurança, com
chmod 400 caminho/nome_arquivo.pem.
```

## Exemplo de comandos pós e após uploade:
```
### pós comando:
# Varial com nome do arquivo ear sig
export SIG_EAR='sigaa'
# Matar java
sudo pkill -9 java && \
# Criar diretorio backup
sudo mkdir ~/backup_ear && \
# Fazer backup do arquivo ear em 
sudo cp /usr/local/sig/applications/${SIG_EAR}.ear ~/backup_ear/${SIG_EAR}.ear-$(date +%d%m%Y%H%M%S) && \
# Remove o arquivo dentro de applications
sudo rm -f /usr/local/sig/applications/${SIG_EAR}.ear && \
# Remove os arquivos temporarios referentes aos ear no jboss, forçando a recriar novos
sudo find /usr/local/sig/jboss-5.1.0.GA/server/default/tmp -type f | grep -v -E "aopdynclasses|vfs-nested.tmp|deploy|service-binding4754572954882927311.tmp" | xargs rm -f && \
# Grava a execução, data no arquivo loader.log
sudo echo "Foi executado o loader ---> $(date +%d%m%Y%H%M%S)" >> ~/loader.log

### após comando:
# Lista arquivos em applications
sudo ls /usr/local/sig/applications/ && \
# Inicia jboss
sudo /etc/init.d/jboss start
```