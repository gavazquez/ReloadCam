#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Arguments, ReloadCam_Helper

def GetVersion():
    return 18

class Server(object):
    def GetUrl():
        pass
    def GetClines(self):
        pass

def CleanupClines(clines):
    clines = filter(None, clines) #Remove "None" lines
    clines = [cline.strip() for cline in clines] #Remove '\n' in all clines
    clines = RemoveRepeatedLines(clines) #Remove duplicated lines
    return clines

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
        if ReloadCam_Helper.TestCline(cline) == False:
            existingClines.remove(cline)

    existingClines = CleanupClines(existingClines)
    clines = CleanupClines(clines)
    print "Found " + str(len(existingClines)) + " working existing clines..."
    print "Retrieved " + str(len(clines)) + " new lines"

    clinesToWrite += clines
    clinesToWrite += existingClines
    clinesToWrite = CleanupClines(clinesToWrite)

    clinesToWrite = ReloadCam_Helper.SortClinesByPing(clinesToWrite)    
    print "Writing a combined total of " + str(len(clinesToWrite)) + " lines to the cccam.cfg!"

    file = open(path, 'w')
    for cline in clinesToWrite:
        file.write(cline + '\n')
    file.close()

def RemoveRepeatedLines(clines):
    clines = list(set(clines))#first remove the ones that are exactly the same    

    #Now remove all the lines that have same hostname and port
    for cline in clines:        
        if ClineAlreadyExists(cline, clines):
            clines.remove(cline)
    return clines

def ClineAlreadyExists(cline, clines):

    host, port = GetHostPort(cline)

    if host is not None and port is not None:
        count = 0
        for currentCline in clines:
            currentHost, currentPort = GetHostPort(currentCline)
            if currentHost is not None and currentPort is not None:
                if host == currentHost and port == currentPort:
                    count += 1
        if count > 1:
            return True

    return False

def GetHostPort(cline):
    import re

    host = None
    port = None

    regExpr = re.compile('[CN]:\s*(\S+)+\s+(\d*)\s+')
    match = regExpr.search(cline)
    if match is not None:
        host = match.group(1)
        port = int(match.group(2))

    return host, port

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
    import sys, os, optparse, ReloadCam_Arguments, platform, traceback, sys

    try:
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

    except Exception,e:
        print "Unexpected error thrown in ReloadCam_Main: " + str(e)
        traceback.print_exc(file=sys.stdout)
    return;

def CleanFiles(currentPath, platform):
    import os, glob
    
    if  platform.lower() == "windows":
        if len(filter(os.path.isfile, glob.glob('./*.pyc'))) > 0:
            os.system('del /q "' + currentPath + '*.pyc"')
        if len(filter(os.path.isfile, glob.glob('./*.pyo'))) > 0:            
            os.system('del /q "' + currentPath + '*.pyo"')
    else:
        os.system("rm -rf " + currentPath + "*.pyc")
        os.system("rm -rf " + currentPath + "*.pyo")

#endregion
