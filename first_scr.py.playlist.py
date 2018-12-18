# required
# pip install BeautifulSoup4
# sudo -H pip install --upgrade youtube-dl
# author: cechus
# date: 04-03-2018

import urllib
import urllib2
import re
import sys
import os
import youtube_dl
import json
from BeautifulSoup import BeautifulSoup


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'verbose': False,
    'ignoreerrors':True
}

url = sys.argv[1]
print bcolors.OKBLUE + "Obteniendo datos de la pagina: " + bcolors.ENDC + bcolors.BOLD+ url + bcolors.ENDC
text = urllib2.urlopen(url).read()
soup = BeautifulSoup(text)
title = soup.find('h1', {
                  'class': 'f1-ns mt0 mb3 pt0 pb0 f2-m f3 fw5 black-90 tc-m'})

if title is None:
    print bcolors.FAIL + "ERROR no se pudo encontrar el titulo de la pagina" + bcolors.ENDC
    exit()

directory = title.text

print bcolors.WARNING + "Verificando si existe el directorio: "  + bcolors.ENDC + bcolors.BOLD + directory + bcolors.ENDC

if not os.path.exists(directory):
    os.makedirs(directory)
    print bcolors.OKGREEN + "Directorio creado "  + bcolors.ENDC

os.chdir(directory)


#print bcolors.HEADER + "Descargando Imagen: " + bcolors.ENDC
json_data = soup.find('script', {
    'class': 'js-react-on-rails-component'
}).text

parsed_json = json.loads(json_data)

#imageUrl = parsed_json['course']['course']['square_cover_large_url']

#if imageUrl is None:

#  print bcolors.FAIL + "ERROR no se pudo encontrar la imagen de la pagina" + bcolors.ENDC
#   exit()
#print imageUrl
#urllib.urlretrieve(imageUrl, os.path.basename(imageUrl))

print bcolors.HEADER + "Obteniendo enlaces: " + bcolors.ENDC
lessons = parsed_json['playlist']['items']
for lesson in lessons:
    print bcolors.OKGREEN + "Descargando video: "+ lesson['title'] + bcolors.ENDC
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        test_url = lesson['url']
        ydl.print_debug_header()
        info = ydl.extract_info(test_url, download=True)

print bcolors.OKGREEN + " -------------------------------- "  + bcolors.ENDC
print len(lessons), "Videos descargados"
