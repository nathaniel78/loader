## Uso do Código:
Este código está disponível para uso com restrições comerciais e requer autorização para modificações.

- **Uso Pessoal e Não Comercial**: Permitido sem a necessidade de autorização.
- **Modificações e Uso Comercial**: Proibidos sem autorização prévia. Para modificações ou uso comercial, entre em contato com [nathanieljose78@gmail.com] para obter permissão.

## Sobre:
```
Loader é um aplicativo para realizar ações pós e após o upload do arquivo.
```

## Instalar:
```
1 - Depois de baixar o projeto, modificar no docker-compose o ALLOWED_HOSTS se necessário.
2 - Executar o comando docker-compose up -d --build
3 - Criar um usuário com o comando docker exec -it loader python manage.py createsuperuser
4 - Campos obrigatório, usuário e password.
5 - Caso necessite resetar a senha docker exec -it loader python manage.py changepassword seu_usuario
6 - Demais comandos docker exec -it loader python manage.py --help
```