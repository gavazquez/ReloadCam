#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

#Para usarlo: 
#1 - Crea un archivo llamado "ReloadCam.py" (La extension debe ser .py!) con algun editor de texto
#2 - Pega todo este texto en ese fichero y guardalo
#3 - Lee todo este texto hasta abajo y haz las correcciones que se indiquen en caso de que sea necesario
#4 - Create otro fichero llamado "RefrescarCcam.sh" (La extension debe ser .sh!) con algun editor de texto
#5 - Desde ese .sh sera desde donde llames al ReloadCam.py, para ello, puedes llamarlo con los estos parametros

#python 'ReloadCam.py' -s mycccam                Refresca el CCcam.cfg con lineas de la web de mycccam
#python 'ReloadCam.py' -s satna                  Refresca el CCcam.cfg con lineas de la web de satna
#python 'ReloadCam.py' -s cccam4you              Refresca el CCcam.cfg con lineas de la web de cccam4you
#python 'ReloadCam.py' -s testious               Refresca el CCcam.cfg con las 5 primeras lineas de la web de testious
#python 'ReloadCam.py' -s freecline              Refresca el CCcam.cfg con las lineas validas de la web de freecline
#python 'ReloadCam.py' -s allcam                 Refresca el CCcam.cfg con las lineas validas de la web de allcam
#python 'ReloadCam.py' -s cccamfree              Refresca el CCcam.cfg con las lineas validas de la web de cccamfree
#python 'ReloadCam.py' -s cccamgenerator         Refresca el CCcam.cfg con las lineas validas de la web de cccamgenerator
#python 'ReloadCam.py' -s all                    Refresca el CCcam.cfg con lineas de todas las web (excepto testious y freecline)
#python 'ReloadCam.py'                           Refresca el CCcam.cfg con lineas de todas las web (excepto testious y freecline)

#Si añades el parametro '--append' (-a) al final, las lineas nuevas solo se añadiran abajo 
#del archivo CCCam.cfg sin borrarlo antes.

#Ejemplo:
#ReloadCam.py -s cccam4you --append
#ReloadCam.py -a

#Con esta llamada tu CCCam.cfg quedaria con las lineas antiguas arriba y las nuevas abajo

#Si ademas le añades el parametro '--check' (-c) se abrira el archivo y borrara las lineas que no esten funcionando
#para luego meter las nuevas lineas debajo

#Ejemplos:
#ReloadCam.py -s cccam4you --append --check
#ReloadCam.py -a -c

#Tu archivo RefrescarCcam.sh deberia quedar con una sola linea
#Ejemplo: ------> python 'ReloadCam.py' -s all

#6 - Sube esos 2 ficheros a /usr/script/ con permisos 755
#7 - Desde el panel de scripts puedes llamarlo o configurarlo para que se ejecute cada X horas en el cron manager.

#-------------------------

#Si quieres poner tus Clines propias, añadelas al metodo GetCustomClines() Tal y como se indica

#-------------------------

#En un futuro seria interesante añadir los 2 servidores de abajo, aunque para eso hay que abrir un zip y leerlas...
#http://free-cccam.tk/MultiUser/cline.php?f=cline/CCcam.zip
#http://free-cccam.tk/MultiUser2/cline.php?f=cline/CCcam.zip

#-------------------------
cccamPath = "C:\Users\gavaz\Desktop\CCcam.cfg"
#cccamPath = "/etc/CCcam.cfg"  #Cambia esta ruta entre comillas en caso necesario pero no la borres!!
cccamBin = "/usr/bin/CCcam_230" #Cambia esta ruta entre comillas en caso necesario pero no la borres!!

def GetCustomClines(): #No borres esta linea!
    customClines = [] #No borres esta linea!

    #-------------------------

    #Añade aqui una o mas custom clines si quieres (puede ser una cline privada o similar) 
    #Ejemplos: (Recuerda borrar el '#')

    #customClines.append('C: micline.no-ip.org 42000 user pass')
    #customClines.append('C: micline2.no-ip.org 42000 user2 pass2')
    #customClines.append('C: micline3.no-ip.org 42000 user3 pass3')
    #customClines.append('N: miNline1.no-ip.org 42000 user1 pass1')

    #-------------------------

    return customClines; #No borres esta linea!

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------- A partir de aqui ya empieza el codigo del script ---------------------
#------------------------------ No lo cambies a menos que sepas lo que haces! ---------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

#region Constants

arguments = ['mycccam','satna','cccam4you','testious','freecline','allcam','cccamfree','cccamgenerator','all']

#endregion

#region Methods

#region Generic methods

def GetHtmlCode(headers, url):
    import urllib, urllib2, cookielib

    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    if headers is not None and len(headers) > 0:
        opener.addheaders = headers
    try:
        htmlCode = opener.open(url).read()
    except:
        print "Could not open website! (No internet connection or bad URL: " + url + ")"
        return '';

    return htmlCode;

def WriteCccamFile(clines, append, check):
    import os, os.path

    existingClines = []
    clinesToWrite = []

    if append and os.path.exists(cccamPath):
        with open(cccamPath) as f:
            existingClines = f.readlines()

    if check: #Check and only write the Clines that are tested
        for cline in existingClines:
            if TestCline(cline) == True:
                clinesToWrite.append(cline)
    else:
        clinesToWrite = existingClines

    for cline in clines:
        if cline is not None and cline != '' and TestCline(cline):
            clinesToWrite.append(cline)

    file = open(cccamPath, 'w')

    for cline in clinesToWrite:
        if not check or (check and TestCline(cline)):
            file.write(cline + '\n')
    file.close()

    print "Finished refreshing the file!"

def GetRandomClines():
    import random
    argument = arguments[random.randint(0,len(arguments)-1)]
    return GetClinesByArgument(argument)

def GetClinesByArgument(argument):
    clines = []
    clines += GetCustomClines()

    if argument == arguments[0]:
        clines += GetMycccamClines()
    elif argument == arguments[1]:
        clines += GetSatnaClines()
    elif argument == arguments[2]:
        clines += GetCccam4youClines()
    elif argument == arguments[3]:
        clines += GetTestiousClines()
    elif argument == arguments[4]:
        clines += GetFreeclineClines() + GetFreeclineNlines()
    elif argument == arguments[5]:
        clines += GetAllcamClines()
    elif argument == arguments[6]:
        clines += GetCccamFreeClines()
    elif argument == arguments[7]:
        clines += GetCccamGeneratorClines()
    else:
        clines += GetMycccamClines() + GetSatnaClines() + GetCccam4youClines() + GetAllcamClines() + \
            GetCccamFreeClines() + GetCccamGeneratorClines()

    return clines

def RestartCccam():
    import time, os
    os.system('killall ' + os.path.basename(cccamBin))
    time.sleep(2)
    os.system('rm -rf /tmp/*.info* /tmp/*.tmp*')
    os.system(cccamBin + ' &')

def TestCline(cline):
    import socket, re, sys

    regExpr = re.compile('[CN]:\s?(\S+)?\s+(\d*)')
    match = regExpr.search(cline)

    if match is None:
        return False;

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        host = match.group(1)
        port = int(match.group(2))
        ip = socket.gethostbyname(host)
        s.connect((ip, port))
        return True
    except:
        s.close()
        return False

    return False

#endregion

#region Mycccam

def GetMycccamClines():
    print "Now getting Myccam clines!"
    myccclineClines = []
    myccclineClines.append(GetMycccamCline(1))
    myccclineClines.append(GetMycccamCline(2))
    myccclineClines.append(GetMycccamCline(3))
    myccclineClines.append(GetMycccamCline(4))
    myccclineClines.append(GetMycccamCline(5))
    myccclineClines.append(GetMycccamCline(6))

    return myccclineClines;

def GetMycccamCline(serverNo):
    import re

    htmlCode = GetHtmlCode(None, "http://www.mycccam24.com/{0}sv2016.php".format(serverNo))
    regExpr = re.compile('Your Free CCcam line is.*C:(.*?)<\/')
    match = regExpr.search(htmlCode)

    if match is None:
        return None;

    cline = match.group(1)

    return 'C:' + cline;

#endregion

#region Satna

def GetSatnaClines():
    print "Now getting Satna clines!"
    satnaClines = []
    satnaClines.append(GetSatnaCline(1))
    satnaClines.append(GetSatnaCline(2))
    satnaClines.append(GetSatnaCline(3))
    satnaClines.append(GetSatnaCline(4))
    satnaClines.append(GetSatnaCline(5))
    satnaClines.append(GetSatnaCline(6))
    return satnaClines;

def GetSatnaCline(serverNo):
    import re

    htmlCode = GetHtmlCode(None, "http://satna4ever.no-ip.biz/satna/nwx{0}.php".format(serverNo))
    regExpr = re.compile('Your Free CCcam line is.*C:(.*?)<\/')
    match = regExpr.search(htmlCode)

    if match is None:
        return None;

    cline = match.group(1)

    return 'C:' + cline;

#endregion

#region Cccam4you

def GetCccam4youClines():
    print "Now getting Cccam4you clines!"
    cccam4youClines = []
    cccam4youClines.append(GetCccam4youCline())
    return cccam4youClines;

def GetCccam4youCline():
    import re

    htmlCode = GetHtmlCode(None, "http://cccam4you.com/FREE/get.php")
    regExpr = re.compile('C:(.*)\r')
    match = regExpr.search(htmlCode)

    if match is None:
        return None;

    cline = match.group(1)

    return 'C:' + cline;

#endregion

#region Testious

def GetTestiousClines():
    import re, time, datetime, random
    print "Now getting Testious clines!"
    clines = []

    header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
    url = "http://www.testious.com/free-cccam-servers/" + datetime.date.today().strftime("%Y-%m-%d")
    htmlCode = GetHtmlCode(header, url)

    regExpr = re.compile('([C]:.*?)#.*\n<br>')
    matches = regExpr.findall(htmlCode)

    while len(matches) < 5:
        yesterday = datetime.date.today() - datetime.timedelta( days = 1 )        
        url = "http://www.testious.com/free-cccam-servers/" + yesterday.strftime("%Y-%m-%d")
        htmlCode = GetHtmlCode(header, url)
        matches = regExpr.findall(htmlCode)

    for i in range(0, 5):
        clines.append(matches[i])

    return clines;

#endregion

#region Freecline

def GetFreeclineClines():
    import re, time, datetime, random
    print "Now getting Freecline clines!"
    clines = []

    header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
    url = "http://www.freecline.com/history/CCcam/" + datetime.date.today().strftime("%Y/%m/%d")
    htmlCode = GetHtmlCode(header, url)

    regExpr = re.compile('Detailed information of the line.*([C]:.*?)<.*\n.*\n.*\n.*\n.*online')
    matches = regExpr.findall(htmlCode)

    while len(matches) < 3:
        yesterday = datetime.date.today() - datetime.timedelta( days = 1 )        
        url = "http://www.freecline.com/history/CCcam/" + yesterday.strftime("%Y/%m/%d")
        htmlCode = GetHtmlCode(header, url)
        matches = regExpr.findall(htmlCode)

    for i in range(0, 3):
        clines.append(matches[i])

    return clines;

def GetFreeclineNlines():
    import re, time, datetime, random
    nlines = []

    header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
    url = "http://www.freecline.com/history/Newcamd/" + datetime.date.today().strftime("%Y/%m/%d")
    htmlCode = GetHtmlCode(header, url)

    regExpr = re.compile('Detailed information of the line.*([N]:.*?)<.*\n.*\n.*\n.*\n.*online')
    matches = regExpr.findall(htmlCode)

    while len(matches) < 3:
        yesterday = datetime.date.today() - datetime.timedelta( days = 1 )        
        url = "http://www.freecline.com/history/Newcamd/" + yesterday.strftime("%Y/%m/%d")
        htmlCode = GetHtmlCode(header, url)
        matches = regExpr.findall(htmlCode)

    for i in range(0, 3):
        nlines.append(matches[i])

    return nlines;

#endregion

#region Allcam

def GetAllcamClines():
    print "Now getting Allcam clines!"
    allcamClines = []
    allcamClines.append(GetAllcamCline(1))
    allcamClines.append(GetAllcamCline(2))
    allcamClines.append(GetAllcamCline(3))
    allcamClines.append(GetAllcamCline(4))
    return allcamClines;

def GetAllcamCline(serverNo):
    import re

    htmlCode = GetHtmlCode(None, "http://www.allcccam.com/serv{0}r.php".format(serverNo))
    regExpr = re.compile('([CN]:\s?\S+?\s+\d*\s?\w+\s?\w+)')
    match = regExpr.search(htmlCode)

    if match is None:
        return None;

    cline = match.group(1)

    return cline;

#endregion

#region CccamFree

def GetCccamFreeClines():
    print "Now getting CccamFree clines!"
    cccamFreeClines = []
    cccamFreeClines.append(GetCccamFreeCline())
    return cccamFreeClines;

def GetCccamFreeCline():
    import re

    htmlCode = GetHtmlCode(None, "http://cccam-free.com/new0.php")
    regExpr = re.compile('([CN]:\s?\S+?\s+\d*\s?\w+\s?\w+)')
    match = regExpr.search(htmlCode)

    if match is None:
        return None;

    cline = match.group(1)

    return cline;

#endregion

#region CccamGenerator

def GetCccamGeneratorClines():
    print "Now getting CccamGenerator clines!"
    cccamGeneratorClines = []
    cccamGeneratorClines.append(GetCccamGeneratorCline())
    return cccamGeneratorClines;

def GetCccamGeneratorCline():
    import re

    htmlCode = GetHtmlCode(None, "http://cccamgenerator.com/generator/get.php")
    regExpr = re.compile('([CN]:\s?\S+?\s+\d*\s?\w+\s?\w+)')
    match = regExpr.search(htmlCode)

    if match is None:
        return None;

    cline = match.group(1)

    return cline;

#endregion

#region Main

def main():
    import sys, os, optparse
    clines = []

    parser = optparse.OptionParser(description="Refrescador automatico de clines. Creado por Dagger")

    possibleArguments = '%s' % ','.join(map(str, arguments))

    parser.add_option('-s', '--server', default='all', dest='web', action='store', choices=arguments,
        help='Especifica la web de la que quieres descargar las clines. Por defecto esta opcion tiene el valor %default que descarga de todas excepto testious y freecline. Valores posibles: ' + possibleArguments)
    
    parser.add_option('-a', '--append', dest='append', default=False, action='store_true',
        help='Mete las nuevas lineas al final sin sobreescribir el CCcam.cfg')

    parser.add_option('-c', '--check', dest='check', default=False, action='store_true', 
        help='Checkea las antiguas lineas del CCcam.cfg y las borra si no funcionan')

    (opts, args) = parser.parse_args()

    if opts.check and not opts.append:
        print "Option check requires option append\n"
        parser.print_help()
        exit(-1)
    
    if opts.web not in arguments:
        print "Bad argument for -s\n"
        parser.print_help()
        exit(-1)
    
    clines = GetClinesByArgument(opts.web)

    if len(clines) > 0:
        print "Now writing to the cccam.cfg!"
        WriteCccamFile(clines, opts.append, opts.check)
        print "Now restarting cam!"
        RestartCccam()
        print "Finished restarting cam!"
    else :
        print "NO CCCAMS LOADED!"
    return;

#endregion

if __name__ == "__main__":
    main()
