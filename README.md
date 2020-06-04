# website-typo-parser
This is a program I wrote a long time ago in Python 2 to detect spelling errors on websites, particularly ones containing files in .xht format.
To install dependencies, simply run `./linuxsetup.sh` or the provided `macossetup.sh`file if you're running macOS. Then, simply run `python typoparser.py` and everything should be all set for you.

This was designed in mind to run `wget` to pull content from Apache-hosted websites and examine them for spelling errors. Simply copy and paste the URL of a specific page and it the program should automatically download the entire website for you (ignoring .mp4, .jpg, .png, and other costly file size formats). This will result in the program freezing briefly and will take a few minutes depending on the size of the website.
![](https://user-images.githubusercontent.com/25623043/82161013-729a7500-9867-11ea-9689-d492d4eac776.png)

To add a word the local dictionary, simply follow the process below and click `Add to Dictionary`.
![](https://user-images.githubusercontent.com/25623043/82161017-762dfc00-9867-11ea-8f9b-45b7f143ea92.png)
