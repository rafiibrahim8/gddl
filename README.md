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
You need to have python 3 installed. `gddl` won't run on python 2.
# USES
You can supply a url to `gddl`.
```sh
gddl "https://drive.google.com/file/d/123MyAwesomeFileID/view?usp=sharing"
```
*Note: Quotes are required for some urls.*

Alternatively, you can download via file ID.
```sh
gddl 123MyAwesomeFileID
```
# ISSUES
If you are facing issue using the program, feel free to create an [issue](https://github.com/rafiibrahim8/gddl/issues). 


# ACKNOWLEDGEMENTS
  - [coursera-dl](https://github.com/coursera-dl/coursera-dl/) project - for their simple and awesome native downloader.
  - [gdown.pl](https://github.com/circulosmeos/gdown.pl/) project - for inspiration of creating this program.

[PyPi-downloads]: https://img.shields.io/pypi/dm/gddl
[PyPi-url]: https://pypi.org/project/gddl/
[License-shield]: https://img.shields.io/github/license/rafiibrahim8/gddl
[License-url]: https://github.com/rafiibrahim8/gddl/blob/master/LICENSE
[PyPi-version]: https://img.shields.io/pypi/v/gddl
