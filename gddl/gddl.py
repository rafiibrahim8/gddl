from .utils import get_session, get_confirmed_url, get_file_info, get_file_id
from .downloaders import get_downloader
from gddl import __version__

import argparse

def download(args):
    file_id = get_file_id(args.url)
    if(not file_id):
        print('The url is invlid.')
        return
    
    api_file_name, api_file_size, error = get_file_info(file_id)
    if(error):
        print('Unable to get the file.\nMake sure you have permission and the url is correct.')
        return
    filename = args.filename if(args.filename) else api_file_name
    
    if(not filename):
        print('Unable to get filename.\n Please re-run the program with -o option.')
        return
       
    session = get_session()
    confirmed_url, error_msg = get_confirmed_url(session, file_id)
    if(error_msg):
        print('Error:', error_msg)
        return
    
    downloader = get_downloader(session, args)
    downloader.download(confirmed_url, filename, args.is_resume, api_file_size)
    session.close()

def main():
    parser = argparse.ArgumentParser(description='Download files from google drive with resuming capability.')
    parser.add_argument('url',help='url of the file to download.')
    parser.add_argument('-x,--no-resume', action='store_false', dest='is_resume', default=True, help='By default gddl will try to resume. Use this flag to stop resuming.')
    parser.add_argument('-o,--filename', dest='filename', default=None, help='Define downloaded filename.')

    parser.add_argument('-v','--version',help='Prints version information.',action='version',version= 'v'+ __version__)

    args = parser.parse_args()
    download(args)

if __name__ == "__main__":
    main()

