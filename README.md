Script fabric para atualização de um proxy de Nginx, fazendo o trabalho que o http://freeddns.noip.com se propõe.

A motivação é que os serviços de dns dinamicos tem o costume de enviar solicitações de confirmação, e suspendem caso o usuário faça a confirmação.

# Instalação:

```
git clone https://github.com/diegotolentino/dynamicdns.git
cd dynamicdns
virtualenv --python=python2.7 venv
venv/bin/pip install -r requirements.txt
```

# Configuração

Adicione as linhas abaixo ao seu arquivo ~/.ssh/config
```
host myhost
  Hostname 123.123.123.1
  Port 22122
  User root  

```

# Utilização

Para configurar o nginx em *myhost* para utilizar o subdomínio *sub.mydomain.com* apontando para sua porta local *80* 
```
venv/bin/fab -H myhost update_dns:domain='sub.mydomain.com',target_port=80
```

Para configurar um outro endereço IP 
```
venv/bin/fab -H myhost update_dns:domain='sub.mydomain.com',target_port=80,target_ip=111.222.121.212
```

Para configurar usando um template diferente 
```
venv/bin/fab -H myhost update_dns:domain='sub.mydomain.com',target_port=80,template=nginx_landare.tpl
```

# Configuração do Crontab

```
0-59/5  *  *  *  *  cd /path/to/dynamicdns/; venv/bin/fab -H myhost update_dns:domain='sub.mydomain.com',target_port=80,template=nginx_landare.tpl
```
