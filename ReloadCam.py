#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Para usarlo: 
#1 - Crea un archivo llamado "ReloadCam.py" (La extension debe ser .py!) con algun editor de texto
#2 - Pega todo este texto en ese fichero y guardalo
#3 - Lee todo este texto hasta abajo y haz las correcciones que se indiquen en caso de que sea necesario
#4 - Create otro fichero llamado "RefrescarCcam.sh" (La extension debe ser .sh!) con algun editor de texto
#5 - Desde ese .sh sera desde donde llames al ReloadCam.py, para ello, puedes llamarlo con los estos parametros (por ejemplo)

#python '/usr/script/ReloadCam.py' -s Mycccam                Refresca el CCcam.cfg con lineas de la web de mycccam
#python '/usr/script/ReloadCam.py' -s Satna -s Mycccam       Refresca el CCcam.cfg con lineas de la web de satna y mycccam

#TODAS (menos testious y freecam): 
#python '/usr/script/ReloadCam.py' -s Mycccam -s Satna -s Cccam4you -s Allcam -s Cccamfree -s Cccamgenerator -s Cccamcafard -s Toopccam -s Kacsat  -s Elaissaoui -s Realtv1 -s Satunivers -s Cccamgratis -s Xhaka -s Greencccamfree -s Jokercccam -s Ultrahd -s Seduct -s Raul7

#Los valores posibles de esos servidores los tienes en el archivo ReloadCam_Arguments.py
#Si todavia no tienes ese fichero, ejecuta el script con cualquier cosa y se te bajaran los archivos necesarios

#Si añades el parametro '--append' (-a) al final, las lineas nuevas solo se añadiran abajo 
#del archivo CCCam.cfg sin borrarlo antes.

#Ejemplo (ambos son iguales):
#ReloadCam.py -s Mycccam --append
#ReloadCam.py -s Mycccam -a

#Con esta llamada tu CCCam.cfg quedaria con las lineas antiguas arriba y las nuevas abajo

#Si ademas le añades el parametro '--check' (-c) se abrira el archivo y borrara las lineas que no esten funcionando
#para luego meter las nuevas lineas debajo

#Ejemplos (ambos son iguales):
#ReloadCam.py -s Mycccam --append --check
#ReloadCam.py -a -c

#Tu archivo RefrescarCcam.sh deberia quedar con una sola linea
#Ejemplo: ------> python '/usr/script/ReloadCam.py' -s Mycccam

#6 - Sube esos 2 ficheros a /usr/script/ con permisos 755
#7 - Desde el panel de scripts puedes llamarlo o configurarlo para que se ejecute cada X horas en el cron manager.
#8 - La primera vez que se ejecute el script se bajaran todos los archivos necesarios para que funcione
#9 - Cada vez que se ejecuta el script se comprueba la ultima version

#-------------------------

#En un futuro seria interesante añadir los servidores de abajo, aunque para eso hay que abrir un zip y leerlas...
#http://free-cccam.tk/MultiUser/cline.php?f=cline/CCcam.zip
#http://free-cccam.tk/MultiUser2/cline.php?f=cline/CCcam.zip

#-------------------------

cccamBin = "/usr/bin/CCcam_230" #Cambia esta ruta entre comillas en caso necesario pero no la borres!!
cccamPath = "/etc/CCcam.cfg"  #Cambia esta ruta entre comillas en caso necesario pero no la borres!!

#Cambia esta ruta SOLO si vas a ejecutar el script en windows. Si lo vas a poner en el vu+ no hace falta que la toques
cccamPathWindows = "C:\Users\gavaz\Desktop\CCcam.cfg"  

#-------------------------

#Si quieres poner tus Clines propias, añadelas al metodo GetCustomClines() Tal y como se indica


def GetCustomClines(): #No borres esta linea!
    customClines = [] #No borres esta linea!

    #Añade aqui una o mas custom clines si quieres (puede ser una cline privada o similar) 
    #Ejemplos: (Recuerda borrar el '#')

    #customClines.append('C: micline.no-ip.org 42000 user pass')
    #customClines.append('C: micline2.no-ip.org 42000 user2 pass2')
    #customClines.append('C: micline3.no-ip.org 42000 user3 pass3')
    #customClines.append('N: miNline1.no-ip.org 42000 user1 pass1')

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

import os.path

sourceUrl = "https://raw.githubusercontent.com/DaggerES/ReloadCam/master/"

#region Refreshing methods

def GetCurrentPath():
    import platform

    currentpath = os.path.dirname(os.path.abspath(__file__))
    if  platform.system().lower()=="windows":
        return currentpath + "\\"
    return currentpath + "/"

def DownloadFile(url):
    import urllib
    try:
        return urllib.urlopen(url).read()
    except:
        print "Could not download file! (No internet connection or bad URL: " + url + ")"
        return None;

def DownloadScript(fileName):
    downloadedScript = DownloadFile(sourceUrl + fileName + ".py")

    if downloadedScript is not None and "Not found" not in downloadedScript:
        newFile = open(GetCurrentPath() + fileName + ".py",'w')
        newFile.write(downloadedScript)
        newFile.close()

def RefreshFiles():
    import ReloadCam_Versions

    print "Comparing local files with latest version..."
    for key in ReloadCam_Versions.Versions.keys():
        fileExists = os.path.isfile(GetCurrentPath() + key + ".py")
        if fileExists is False: #File not exists so download it
            print "File not found! Downloading script with filename: " + key
            DownloadScript(key)
        else:   #File exists so check version number
            currentVersion = GetScriptVersion(GetCurrentPath() + key + ".py")
            if ReloadCam_Versions.Versions[key] > currentVersion:
                print "Old version found! Downloading script with filename: " + key
                DownloadScript(key)

def GetScriptVersion(path):
    execfile(path)
    try:
        version = locals()["GetVersion"]()
        return version
    except:
        print "ERROR! Could not get version number for file " + path
        return 9999;

#endregion

#region Main

def Main():
    import ReloadCam_Main, platform
    
    if  platform.system().lower() == "windows": #Esto es solo por si lo ejecutas en windows
        ReloadCam_Main.Main(GetCustomClines(), cccamPathWindows, cccamBin)
    else:
        ReloadCam_Main.Main(GetCustomClines(), cccamPath, cccamBin)

    ReloadCam_Main.Cleanup(GetCustomClines(), cccamPath, cccamBin)

#endregion

if __name__ == "__main__":
    print "Getting latest file versions and checking for updates..."
    DownloadScript("ReloadCam_Versions")
    RefreshFiles()
    Main()
