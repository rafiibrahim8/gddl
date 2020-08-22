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
###### Hiding 'Hello World!' inside infile.mp3. The resultant file is outfile.wav
#### 
```sh
$ gddl https://drive.google.com/open?id=abcde12345
```

# DEPENDENCY
  - requests
  - urllib3
