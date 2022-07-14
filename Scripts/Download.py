# Download raw texts from urls (for example, my Emacs config files)
# Python should already be installed.
# how to use: <your command prompt> >python Download.py
import urllib.request
urls = ['https://raw.githubusercontent.com/Br41nfck/.emacs.d/main/config.el',
        'https://raw.githubusercontent.com/Br41nfck/.emacs.d/main/config.org',
        'https://raw.githubusercontent.com/Br41nfck/.emacs.d/main/README.md']
for url in urls:
    if url.find('/'):
        name = url.rsplit('/', 1)[1]
        print(name)
        urllib.request.urlretrieve(url, name)
print("Done!")
