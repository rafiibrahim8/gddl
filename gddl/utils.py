import requests
import ssl
import re
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from html.parser import HTMLParser

GOOGLE_API_URL = 'https://content.googleapis.com/drive/v2/files/'
GOOGLE_API_PARAMS = {'key': 'AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM'}
GOOGLE_API_HEADERS = {
    'X-Origin': 'https://explorer.apis.google.com',
    'X-Referer': 'https://explorer.apis.google.com'
}

REG_EX = '([0-9A-Za-z_-]{18,})'

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = False
    
    def get_title(self):
        return self.title
    
    def handle_starttag(self, tag, attrs):
        if(tag.lower() == 'title'):
            self.recording = True

    def handle_endtag(self, tag):
        if(tag.lower() == 'title'):
            self.recording = False
    
    def handle_data(self, data):
        if(self.recording):
            self.title = data

def get_html_title(html_page):
    title_parser = TitleParser()
    title_parser.feed(html_page)
    return title_parser.get_title()

def get_file_id(url):
    match = re.findall(REG_EX, url)
    if(match):
        return match[0]
    return None

def __get_direct_url(file_id):
        return 'https://drive.google.com/uc?export=download&id={}'.format(file_id)

def get_confirmed_url(session, file_id):
    url = __get_direct_url(file_id)
    head = session.head(url).headers

    location = head.get('Location') or head.get('location')
    if(location):
        return location, None
        
    res = session.get(url).content.decode()
    for i in res.split('&amp;'):
        if i.startswith('confirm'):
            return url+'&'+i, None
    return None, get_html_title(res)

def get_file_info(file_id):
    res = requests.get(GOOGLE_API_URL + file_id, headers = GOOGLE_API_HEADERS, params=GOOGLE_API_PARAMS).json()
    if(res.get('error')):
        return None, None, True
    file_name = res.get('title')
    file_size = res.get('fileSize')
    file_size = int(file_size) if(file_size) else file_size

    return file_name, file_size, False

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

