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
#python '/usr/script/ReloadCam.py' -s ALL                    Refresca el CCcam.cfg con lineas de todas las webs
#python '/usr/script/ReloadCam.py' -s ALLTF                  Refresca el CCcam.cfg con lineas de todas las webs excepto testious y freecline

#Los valores posibles de esos servidores los tienes en el archivo ReloadCam_Arguments.py
#Si todavia no tienes ese fichero, ejecuta el script con cualquier parametro y se te bajaran los archivos necesarios

#Si añades el parametro '--norestart' (-r) al final, el CCCam no se reiniciara despues del refresco
#Ejemplo: python '/usr/script/ReloadCam.py' -s ALLTF --norestart
----

#6 - Sube esos 2 ficheros (tanto el .sh como este .py) a /usr/script/ con permisos 755
#7 - Desde el panel de scripts puedes llamarlo o configurarlo para que se ejecute cada X horas en el cron manager.
#8 - La primera vez que se ejecute el script se bajaran todos los archivos necesarios para que funcione
#9 - Cada vez que se ejecuta el script se comprueba la ultima version y se eliminan los archivos que no se necesitan

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
    import ReloadCam_Main, platform
    
    try:
        if  platform.system().lower() == "windows": #Esto es solo por si lo ejecutas en windows
            ReloadCam_Main.Main(GetCustomClines(), cccamPathWindows, cccamBin)
        else:
            ReloadCam_Main.Main(GetCustomClines(), cccamPath, cccamBin)
    except Exception,e:
        print "Unexpected error: " + str(e)
    finally:
        ReloadCam_Main.CleanFiles(GetCurrentPath(), platform.system())

#endregion

if __name__ == "__main__":
    print "Getting latest file versions and checking for updates..."
    DownloadScript("ReloadCam_Versions")
    RefreshFiles()
    Main()
