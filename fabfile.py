# Encoding: UTF-8
"""
Usage:
    fab [target] [action ...]

fab --list
fab -H your_ssh_host update_dns:domain='sub.mydomain.com',target_port=80,target_ip=111.222.121.212
fab -H your_ssh_host update_dns:domain='sub.mydomain.com',target_port=80
"""
import urllib2
from StringIO import StringIO

from fabric.contrib import files
from fabric.api import *
from jinja2 import Template

##############################################################################
# Configurations
##############################################################################
env.use_ssh_config = True # Procura hosts no arquivo ~/.ssh/config

##############################################################################
# Tarefas executaveis
##############################################################################
@task
def get_local_ip():
    get_ip_url = 'http://ipinfo.io/ip'
    try:
        response = urllib2.urlopen(get_ip_url)
    except:
        raise Exception(u'Endereço "%s" não pode ser aberto' % get_ip_url)

    assert response.getcode() == 200

    local_ip = response.read().strip()
    ip_token = local_ip.split('.')
    assert len(ip_token) == 4

    for toke in ip_token:
        assert toke.isdigit()

    return local_ip


@task
def update_dns(domain, target_port=80, target_ip=None, template='nginx.tpl'):
    """ Atualiza o proxy do nginx """

    if not target_ip:
        target_ip = get_local_ip()

    kwargs = {
        'domain': domain,
        'target_port': target_port,
        'target_ip': target_ip
    }

    files.upload_template(
        filename=template,
        destination='/etc/nginx/sites-enabled/dynamicdns.' + domain,
        context=kwargs,
        use_jinja=True,
        backup=False
    )

    run('/etc/init.d/nginx configtest && /etc/init.d/nginx reload')
