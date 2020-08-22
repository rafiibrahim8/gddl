from .utils import get_session, get_confirmed_url, get_filename
from .downloaders import get_downloader
from gddl import __version__

import argparse

def download(args):
    session = get_session()
    confirmed_url = get_confirmed_url(session, args.url)
    filename = args.filename if(args.filename) else get_filename(session, confirmed_url)
    
    if(not filename):
        print('Unable to get filename from HTTP headers.\n Please re-run the program with -o option.')
        exit()
    
    downloader = get_downloader(session, args)
    downloader.download(confirmed_url, filename, args.is_resume)
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

