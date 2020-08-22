import requests
import ssl
import re
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

reg_exs = [
    '^https?://drive.google.com/file/d/([^/]+)',
    'id=([^/&]+)'
]

def __get_file_id(url):
    for i in reg_exs:
        match = re.findall(i, url)
        if(match):
            return match[0]
    
    return None

def __get_direct_url(url):
    id = __get_file_id(url)
    if(id==None):
        print('The entered url is invalid.')
        exit()
    else:
        return 'https://drive.google.com/uc?export=download&id={}'.format(id)

def get_confirmed_url(session, url):
    url = __get_direct_url(url)
    head = session.head(url).headers

    if(not head.get('Location')):
        res = session.get(url).content.decode()
        for i in res.split('&amp;'):
            if i.startswith('confirm'):
                return url+'&'+i
        return None
    
    else:
        return url

def get_filename(session, confirmed_url):    
    try:
        print('Getting filename from HTTP headers.')
        head = session.get(confirmed_url, stream=True).headers
        for i in head.get('Content-Disposition').split(';'):
            if(i.startswith('filename=')):
                return i.split('=')[1].replace('"','')
    except:
        return None


class TLSAdapter(HTTPAdapter):
    # Copyright (C) 2007 Free Software Foundation
    # Class is copied from: https://github.com/coursera-dl/coursera-dl/blob/master/coursera/cookies.py , Under LGPLv3+ License
    # You may get a copy of the license here: https://github.com/coursera-dl/coursera-dl/blob/master/LICENSE

    """
    A customized HTTP Adapter which uses TLS v1.2 for encrypted
    connections.
    """

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_2)


def get_session():
    session = requests.Session()
    session.mount('https://', TLSAdapter())
    return session

