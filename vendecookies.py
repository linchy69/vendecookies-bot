# -*- coding: utf-8 -*-
import requests
import re
import time
import sys
from config import USERNAME, PASSWORD

BASE_URL = 'http://www.vendecookies.com/'
LOGIN_URL = BASE_URL + 'index.php'
HOME_URL = BASE_URL + 'index.php?p=cocinar'
RESOURCE_URL = BASE_URL + 'ws/ObtainResource.php'
REGEXP = re.compile('index.php\?p=cocinar&r=[2-6]&h=(.*)')
TITULO_EXP = re.compile('<div class="titulo">(.*)</div>')
RESULT_EXP = re.compile('imatges/disseny/(.*)-0[2-6].png')
FALTA_EXP = re.compile('falta" id="ing-(.*)">')
resources = [2, 3, 4, 5, 6]

def post_token(token):
    token = token.replace('";', '')
    token = token.replace('\'></div>', '')
    for delimiter in ('else', ';"'):
        del_pos = token.find('else')
        if del_pos >= 0:
	    token = token[:del_pos]
    if 'suerte' in token:
        token = token[:32]
    if '+hash+' in token:
        print 'Please complete manually some effors'
        sys.exit(1)
    print HOME_URL+'&r=%d&h=%s' % (resource, token)
    response = s.get(HOME_URL+'&r=%d&h=%s' % (resource, token))
    result, = RESULT_EXP.findall(response.text)
    print result

with requests.session() as s:
    s.headers.update({
        'Host': 'www.vendecookies.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0',
    })
    # fetch the login page
    s.get(BASE_URL)

    # post to the login form
    r = s.post(BASE_URL, data={
	    'entrar': 'INICIAR+SESIÓN',
	    'usuario': USERNAME,
	    'password': PASSWORD,
	})
    while True:
        hashes = 0
        for resource in resources:
            #time.sleep(1)
            r = s.get(HOME_URL)
            falta = FALTA_EXP.findall(r.text)
            if falta:
                resource = int(falta[0])
            #time.sleep(2)
            response = s.post(RESOURCE_URL, data={
                'resource':resource,
            }, headers={
                'Referer': 'http://www.vendecookies.com/index.php?p=cocinar&r=%d' % resource,
            })
            groups = REGEXP.findall(response.text)
            
            titulos = TITULO_EXP.findall(response.text)
            if titulos:
                titulo, = titulos
            else:
                titulo = 'Regalo'
            print titulo
            token = None
	    if len(groups) == 1:
                token, = groups
                post_token(token)
            elif titulo == 'Ahorcado':
                token = groups[0]
                post_token(token)
            elif 's es menos' in titulo:
                token = groups[0]
                post_token(token)
	    else:
                token = groups[0]
                post_token(token)
        print 'Compleeted one resource loop', hashes
