#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Arguments, ReloadCam_Helper

def GetVersion():
    return 10

class Server(object):
    def GetUrl():
        pass
    def GetClines(self):
        pass

def WriteCccamFile(clines, path):
    """Crea el archivo CCCam.cfg"""
    import os, os.path

    existingClines = []
    clinesToWrite = []

    if os.path.exists(path):
        with open(path) as f:
            existingClines = f.readlines()
    
    print "Testing " + str(len(existingClines)) + " existing clines..."
    for cline in existingClines:
        if ReloadCam_Helper.TestCline(cline) == True:
            clinesToWrite.append(cline)

    clinesToWrite += clines
    clinesToWrite = filter(None, clinesToWrite) #Remove "None" lines
    clinesToWrite = [cline.strip() for cline in clinesToWrite] #Remove '\n' in all clines
    clinesToWrite = list(set(clinesToWrite)) #Remove duplicated lines
    clinesToWrite = ReloadCam_Helper.SortClinesByPing(clinesToWrite)    
    print "Writing a total of " + str(len(clinesToWrite)) + " lines to the cccam.cfg!"

    file = open(path, 'w')
    for cline in clinesToWrite:
        file.write(cline + '\n')
    file.close()

def GetClinesByArgument(arguments, customClines):
    """Lee los arguments y carga las clines pertinentes"""
    import importlib

    clines = []
    clines += customClines #Primero agregamos las clines custom

    if len(arguments) > 1 and ('ALL' in arguments or 'ALLTF' in arguments):
        print "Cannot use parameter ALL/ALLTF with other parameters"
        return clines
    elif len(arguments) == 1 and 'ALL' in arguments:
        arguments = ReloadCam_Arguments.Arguments
        arguments.remove('ALL')
        arguments.remove('ALLTF')
    elif len(arguments) == 1 and 'ALLTF' in arguments:
        arguments = ReloadCam_Arguments.Arguments
        arguments.remove('ALL')
        arguments.remove('ALLTF')
        arguments.remove('Testious')
        arguments.remove('Freecline')

    for argument in arguments:
        moduleName = 'ReloadCam_Server_' + argument #creamos el nombre del modulo que tenemos que importar ej:ReloadCam_Myccam
        my_module = importlib.import_module(moduleName) #Esta linea importa el modulo como si hicieramos un import <nombremodulo>
        classInstance = getattr(my_module, argument)() #Creamos una instancia de ese modulo importado
        clines += classInstance.GetClines() #Este metodo lo deben implementar todas las clases derivadas de "Server"

    return clines

def RestartCccam(path):
    """Resetea el proceso de CCCam para que las nuevas clines se carguen"""
    import time, os

    if os.path.exists(path):
        os.system('killall ' + os.path.basename(path))
        time.sleep(0.5)
        os.system('rm -rf /tmp/*.info* /tmp/*.tmp*')
        os.system(path + ' &')
    else:
        print "ERROR! Cannot restart cccam! Restart manually or fix variable path cccamBin! Current value: " + path

def Main(customClines, cccamPath, cccamBin):
    import sys, os, optparse, ReloadCam_Arguments, platform
    clines = []

    parser = optparse.OptionParser(description="Refrescador automatico de clines. Creado por Dagger")

    possibleArguments = '%s' % ','.join(map(str, ReloadCam_Arguments.Arguments))

    parser.add_option('-s', '--server', dest='web', action='append', choices=ReloadCam_Arguments.Arguments,
        help="Especifica la web de la que quieres descargar las clines. Puedes repetir este parametro varias \
            veces o usar ALL para llamar a todos o ALLTF para todos menos testious y feecline. Valores posibles: " + possibleArguments)

    parser.add_option('-r', '--norestart', dest='norestart', default=False, action='store_true', 
        help='NO reinicia la cccam despues del refresco de clines')

    (opts, args) = parser.parse_args()

    clines = GetClinesByArgument(opts.web, customClines)

    if len(clines) <= 0:
        print "CAUTION! No new lines retrieved"
    
    WriteCccamFile(clines, cccamPath)
    if opts.norestart is False and platform.system().lower() != "windows":
        print "Restarting cam!"
        RestartCccam(cccamBin)
    print "Finished!!!"

    return;

def CleanFiles(currentPath, platform):
    import os, glob

    if len(filter(os.path.isfile, glob.glob('./*.pyc'))) > 0:
        if  platform.lower() == "windows":
            os.system('del /q "' + currentPath + '*.pyc"')
        else:
            os.system("rm -rf " + currentPath + "*.pyc")

    if len(filter(os.path.isfile, glob.glob('./*.pyo'))) > 0:
        if  platform.lower() == "windows":
            os.system('del /q "' + currentPath + '*.pyo"')
        else:
            os.system("rm -rf " + currentPath + "*.pyo")

#endregion
