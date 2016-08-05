#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Arguments, ReloadCam_Helper

def GetVersion():
    return 31

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
        file.write(cline)
        file.write('\n')
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
    import ReloadCam_Importlib

    clines = []
    clines += customClines #Primero agregamos las clines custom

    if arguments is None:
        print "No parameters supplied!"
        return clines

    if len(arguments) > 1 and ('ALL' in arguments or 'ALLTF' in arguments or 'ALLT' in arguments or 'ALLF' in arguments):
        print "Cannot use parameter ALL/ALLTF/ALLT/ALLF with other parameters"
        return clines
    else:
        if 'ALL' in arguments:
            arguments = ReloadCam_Arguments.Arguments
            arguments.remove('ALL')
            arguments.remove('ALLT')
            arguments.remove('ALLF')
            arguments.remove('ALLTF')
        if 'ALLT' in arguments:
            arguments = ReloadCam_Arguments.Arguments
            arguments.remove('ALL')
            arguments.remove('ALLT')
            arguments.remove('ALLF')
            arguments.remove('ALLTF')
            arguments.remove('Testious')
        if 'ALLF' in arguments:
            arguments = ReloadCam_Arguments.Arguments
            arguments.remove('ALL')
            arguments.remove('ALLT')
            arguments.remove('ALLF')
            arguments.remove('ALLTF')
            arguments.remove('Freecline')
        if 'ALLTF' in arguments:
            arguments = ReloadCam_Arguments.Arguments
            arguments.remove('ALL')
            arguments.remove('ALLT')
            arguments.remove('ALLF')
            arguments.remove('ALLTF')
            arguments.remove('Testious')
            arguments.remove('Freecline')
            
    for argument in arguments:
        moduleName = 'ReloadCam_Server_' + argument #creamos el nombre del modulo que tenemos que importar ej:ReloadCam_Myccam
        try:
            my_module = ReloadCam_Importlib.import_module(moduleName) #Esta linea importa el modulo como si hicieramos un import <nombremodulo>
            classInstance = getattr(my_module, argument)() #Creamos una instancia de ese modulo importado
            clines += classInstance.GetClines() #Este metodo lo deben implementar todas las clases derivadas de "Server"
        except Exception,e:
            print "Error loading module: " + moduleName
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

        parser.add_option('-o', '--oscam', dest='oscam', help='Traduce el cccam.cfg a formato OSCAM y lo guarda en la ruta que le indiques')

        parser.add_option('-r', '--norestart', dest='norestart', default=False, action='store_true', 
            help='NO reinicia la cccam despues del refresco de clines')

        parser.add_option('-n', '--nodownload', dest='nodownload', default=False, action='store_true', 
            help='NO descarga nuevas lineas. Solo reordena por ping y elimina las lineas que no funcionan')

        (opts, args) = parser.parse_args()

        if opts.nodownload is True and opts.web is not None:
            print "Cannot call with -s and -n at the same time"
            return;
        
        if opts.nodownload is False:
            clines = GetClinesByArgument(opts.web, customClines)
            if len(clines) <= 0:
                print "CAUTION! No new lines retrieved"
    
        WriteCccamFile(clines, cccamPath)

        if opts.oscam is not None:
            TransformToOscamFile(opts.oscam, cccamPath)

        if opts.norestart is False and platform.system().lower() != "windows":
            print "Restarting cam!"
            RestartCccam(cccamBin)
        print "Finished!!!"

    except Exception,e:
        print "Unexpected error thrown in ReloadCam_Main: " + str(e)
        traceback.print_exc(file=sys.stdout)
    return;

def TransformToOscamFile(oscamPath, cccamPath):
    import re, os

    if os.path.exists(cccamPath):
        file = open(oscamPath, 'w')
        for line in open(cccamPath,'r').readlines():
            cline = re.match(r'(.*)C: (.*?) (.*?) (.*?) (.*)',line)
            if cline:            
                file.write("\n")
                file.write("[reader]"+"\n")
                file.write("enable = 1"+"\n")
                file.write("label = "+ cline.group(2)+"\n")
                file.write("protocol = cccam"+"\n")         
                file.write("device = "+cline.group(2)+","+cline.group(3)+"\n")
                file.write("user = "+cline.group(4)+"\n")
                file.write("password = "+cline.group(5)+"\n")
                file.write("inactivitytimeout = 5"+"\n")
                file.write("reconnecttimeout = 5"+"\n")
                file.write("group = 1"+"\n")
                file.write("emmcache = 1,3,2,0"+"\n")
                file.write("blockemm-unknown = 1"+"\n")
                file.write("blockemm-u = 1"+"\n")
                file.write("blockemm-s = 1"+"\n")
                file.write("blockemm-g = 1"+"\n")
                file.write("cccversion = 2.0.11"+"\n")
                file.write("ccckeepalive = 1"+"\n")
        file.close()

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
