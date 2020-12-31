[![PyPi Downloads][PyPi-downloads]][PyPi-url]
[![PyPi Version][PyPi-version]][PyPi-url]
[![License][License-shield]][License-url]

# gddl
#### Download files from google drive with resuming capability.

# DESCRIPTION
This program can be used for downloading files (including large files) from google drive using the command line. The program supports resuming which is lacking in most of the command line google drive downloaders. 
# INSTALLATION
From a command line enter the command to install gddl
```
pip install gddl
```
You need to have python 3 installed. gddl won't run on python 2.
# USES

```sh
$ gddl "https://drive.google.com/open?id=abcde12345"
```
*Note: Quotes are required for some urls.*

# DEPENDENCY
  - requests
  - urllib3

# ACKNOWLEDGEMENTS
  - [gdown.pl](https://github.com/circulosmeos/gdown.pl/) project - for regular expression to extract file id form url.
  - [coursera-dl](https://github.com/coursera-dl/coursera-dl/) project - for their simple and awesome native downloader.

[PyPi-downloads]: https://img.shields.io/pypi/dm/gddl
[PyPi-url]: https://pypi.org/project/gddl/
[License-shield]: https://img.shields.io/github/license/rafiibrahim8/gddl
[License-url]: https://github.com/rafiibrahim8/gddl/blob/master/LICENSE
[PyPi-version]: https://img.shields.io/pypi/v/gddl
