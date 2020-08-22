from setuptools import setup
from gddl import __version__

def read_file(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            return f.read()
    except:
        return []

requirements = read_file('requirements.txt')
long_description = read_file('README.md')

setup(
    name='gddl',
    version=__version__,
    
    author='Ibrahim Rafi',
    author_email='me@ibrahimrafi.me',

    license='MIT',

    url='https://github.com/rafiibrahim8/gddl',
    download_url = 'https://github.com/rafiibrahim8/gddl/archive/v{}.tar.gz'.format(__version__),

    install_requires=requirements,

    description='Download files from google drive with resuming capability.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gddl', 'downloader', 'drive', 'google'],

    packages=["gddl"],
    entry_points=dict(
        console_scripts=[
            'gddl=gddl.gddl:main'
        ]
    ),

    platforms=['any'],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Utilities',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
