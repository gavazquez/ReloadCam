#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Creado por 'Dagger'

#- Script para refrescar lineas desde python para Vu+/Qviart. Permite refrescarlas desde el mando a 
#distancia o con el CronManager a una hora fijada.

#- Foro de discusion del script: http://www.forokeys.com/foro/vu/refrescar-cclines-automaticamente

#- Url del repositiorio: https://github.com/gavazquez/ReloadCam

#- El script es de codigo libre por lo que si quieres comprobar como NO 
#envia tus Clines a nadie puedes verlo por ti mismo en la url del repositorio (es necesario que tengas conocimientos de python)

#- El script NO inserta las lineas que NO funcionan por lo cual puede parecer que no inserta casi lineas, 
#lo que pasa es que una vez ha obtenido las lineas de una web, comprueba si estas funcionan o no y no inserta las que no funcionan.

#- Cuando testea las lineas, las testea internamente, NO las envia ni a testious ni a otro tipo de webs "sospechosas"

#IMPORTANTE!!! este simbolo -----> #    Son COMENTARIOS en python, son simplemente para que el python lo ignore,
#esto significa que en tus scripts .sh NO debes ponerlo!

#Para usarlo: 
#1 - Crea un archivo llamado "ReloadCam.py" (La extension debe ser .py!) con algun editor de texto
#2 - Pega INTEGRAMENTE (desde el principio hasta el final) este texto en ese fichero y guardalo
#3 - Lee todo este texto hasta abajo y haz las correcciones que se indiquen en caso de que sea necesario
#4 - Create otro fichero llamado "RefrescarCcam.sh" (La extension debe ser .sh!) con algun editor de texto
#5 - Desde ese .sh sera desde donde llames al ReloadCam.py, para ello, puedes llamarlo con los estos parametros (por ejemplo)

#(Recuerda borrar el simbolo ----> #)
#python '/usr/script/ReloadCam.py' -s Allcam                Refresca el CCcam.cfg con lineas de la web de allcam
#python '/usr/script/ReloadCam.py' -s Mario -s Allcam       Refresca el CCcam.cfg con lineas de la web de mario y allcam

#TODAS (menos testious y freecam): 
#python '/usr/script/ReloadCam.py' -s ALLTF

#TODAS (menos testious): 
#python '/usr/script/ReloadCam.py' -s ALLF

#TODAS (menos freecam): 
#python '/usr/script/ReloadCam.py' -s ALLT

#TODAS (incluidas testious y freecam): 
#python '/usr/script/ReloadCam.py' -s ALL

#Los valores posibles de esos servidores los tienes en el archivo ReloadCam_Arguments.py
#Si todavia no tienes ese fichero, ejecuta el script con cualquier cosa y se te bajaran los archivos necesarios

#Si ademas le añades el parametro '--norestart' (-r) el CCCam NO se reiniciara despues de actualizar las lineas

#Ejemplos (ambos son iguales):
#ReloadCam.py -s Mario --norestart
#ReloadCam.py -s Mario -r

#Si quieres usar OSCAM en vez de cccam debes usarlo con el parametro -o "RUTAALOSCAM.SERVER" ejemplos (ambos son iguales):
#ReloadCam.py -s ALL -o "/etc/tuxbox/config/oscam.server"
#ReloadCam.py -s ALL --oscam "/etc/tuxbox/config/oscam.server"

#IMPORTANTE!!!  Tu archivo RefrescarCcam.sh deberia quedar con una sola linea y sin ningun simbolo ------> #
#Ejemplo: ------> python '/usr/script/ReloadCam.py' -s ALLTF

#6 - Sube esos 2 ficheros a /usr/script/ con permisos 755
#7 - Desde el panel de scripts puedes llamarlo o configurarlo para que se ejecute cada X horas en el cron manager.
#8 - La primera vez que se ejecute el script se bajaran todos los archivos necesarios para que funcione
#9 - Cada vez que se ejecuta el script se comprueba la ultima version

#-------------------------

cccamBin = "/usr/bin/CCcam_230" #Cambia esta ruta entre comillas en caso necesario pero no la borres!!
cccamPath = "/etc/CCcam.cfg"  #Cambia esta ruta entre comillas en caso necesario pero no la borres!!

#Cambia esta ruta SOLO si vas a ejecutar el script desde windows. Si lo vas a poner en el vu+ no hace falta que la toques
cccamPathWindows = "C:\Users\gavaz\Desktop\CCcam.cfg"  

#-------------------------

#Si quieres poner tus Clines propias, añadelas al metodo GetCustomClines() Tal y como se indica

def GetCustomClines(): #No borres esta linea!
    customClines = [] #No borres esta linea!

    #Añade aqui una o mas custom clines si quieres (puede ser una cline privada o similar)
    #Respeta las comillas al inicio y final de esta!
    
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

sourceUrl = "https://raw.githubusercontent.com/gavazquez/ReloadCam/master/"

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
    import ReloadCam_Versions, platform

    for key in ReloadCam_Versions.Versions.keys():
        fileExists = os.path.exists(GetCurrentPath() + key + ".py")
        if ReloadCam_Versions.Versions[key] <= 0: #If version is "0" means that we must delete the file
            if fileExists is True:
                print "Removing file: " + key
                if  platform.system().lower() == "windows":
                    os.system('del /q "' + GetCurrentPath() + key + '.py"')
                else:
                    os.system('rm -rf "' + GetCurrentPath() + key + '.py"')
        else:
            currentVersion = GetScriptVersion(GetCurrentPath() + key + ".py")
            if currentVersion == 0:
                print "File not found! Downloading script with filename: " + key
                DownloadScript(key)
            elif currentVersion > 0 and ReloadCam_Versions.Versions[key] > currentVersion:
                print "Old version (" + str(currentVersion) + ") found! " + \
                        "Downloading new version (" + str(ReloadCam_Versions.Versions[key]) + ") for filename: " + key
                DownloadScript(key)

def GetScriptVersion(path):
    try:
        execfile(path)
        version = locals()["GetVersion"]()
        return version
    except:
        return 0;

#endregion

#region Main

def Main():
    import ReloadCam_Main, platform, traceback, sys
    
    try:
        if  platform.system().lower() == "windows": #Esto es solo por si lo ejecutas en windows
            ReloadCam_Main.Main(GetCustomClines(), cccamPathWindows, cccamBin)
        else:
            ReloadCam_Main.Main(GetCustomClines(), cccamPath, cccamBin)
    except Exception,e:
        print "Unexpected error in ReloadCam: " + str(e)
        traceback.print_exc(file=sys.stdout)
    finally:
        ReloadCam_Main.CleanFiles(GetCurrentPath(), platform.system())

#endregion

#region Other Methods

def InternetConnected():
    import urllib2

    try:
        response = urllib2.urlopen('http://www.google.com',timeout=5)
        return True
    except:
        pass
    return False

#endregion

if __name__ == "__main__":
    if InternetConnected():
        print "Getting latest file versions and checking for updates..."
        DownloadScript("ReloadCam_Versions")
        RefreshFiles()
        Main()
    else:
        print "No internet connection!"
