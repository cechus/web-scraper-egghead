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


url = sys.argv[1]
print bcolors.OKBLUE + "Obteniendo datos de la pagina: " + bcolors.ENDC + bcolors.BOLD+ url + bcolors.ENDC
text = urllib2.urlopen(url).read()
soup = BeautifulSoup(text)
title = soup.find('div', {
                  'class': 'f4 f3-m f2-l mt3 mb4 mt0-l avenir fw6 lh-title flex items-center base'})
if title is None:
    print bcolors.FAIL + "ERROR no se pudo encontrar el titulo de la pagina" + bcolors.ENDC
    exit()

directory = title.text

print bcolors.WARNING + "Verificando si existe el directorio: "  + bcolors.ENDC + bcolors.BOLD + directory + bcolors.ENDC

if not os.path.exists(directory):
    os.makedirs(directory)
    print bcolors.OKGREEN + "Directorio creado "  + bcolors.ENDC

os.chdir(directory)
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'verbose': True,
    'ignoreerrors':True
}


print bcolors.HEADER + "Descargando Imagen: " + bcolors.ENDC
imageUrl = soup.find('img', {'class': re.compile('courseIllustration')})['src']
urllib.urlretrieve(imageUrl, os.path.basename(imageUrl))

print bcolors.HEADER + "Obteniendo enlaces: " + bcolors.ENDC
div = soup.find('div', attrs={'class': re.compile('courseInfoLessonList')})

links = div.findAll('a', {'class': re.compile('lh-title')})
for a in links:
    videe = "https://egghead.io" +a['href']
    print bcolors.OKGREEN + "Descargando: "+ videe + bcolors.ENDC
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        test_url = videe
        ydl.print_debug_header()
        info = ydl.extract_info(test_url, download=False)

print bcolors.OKGREEN + " -------------------------------- "  + bcolors.ENDC
print len(links), "Videos procesados"
