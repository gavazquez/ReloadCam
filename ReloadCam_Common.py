#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Arguments, ReloadCam_Helper

def GetVersion():
    return 1

class Server(object):
    def GetUrl():
        pass
    def GetClines(self):
        pass

def WriteCccamFile(clines, append, check, path):
    """Crea el archivo CCCam.cfg"""
    import os, os.path

    existingClines = []
    clinesToWrite = []

    if append and os.path.exists(path):
        with open(path) as f:
            existingClines = f.readlines()
    
    existingClines = filter(None, existingClines)

    for cline in existingClines:
        if check == False or (check == True and TestCline(cline) == True):
            clinesToWrite.append(cline)

    clinesToWrite += clines
    clinesToWrite = ReloadCam_Helper.SortClinesByPing(clinesToWrite)

    file = open(path, 'w')
    for cline in clinesToWrite:
        file.write(cline + '\n')
    file.close()

def GetClinesByArgument(arguments, customClines):
    """Lee los arguments y carga las clines pertinentes"""
    import importlib

    clines = []
    clines += customClines #Primero agregamos las clines custom

    for argument in arguments:
        moduleName = 'ReloadCam_' + argument #creamos el nombre del modulo que tenemos que importar ej:ReloadCam_Myccam
        my_module = importlib.import_module(moduleName) #Esta linea importa el modulo como si hicieramos un import <nombremodulo>
        classInstance = getattr(my_module, argument)() #Creamos una instancia de ese modulo importado
        clines += classInstance.GetClines() #Este metodo lo deben implementar todas las clases derivadas de "Server"

    return clines

def RestartCccam(path):
    """Resetea el proceso de CCCam para que las nuevas clines se carguen"""
    import time, os

    if os.path.exists(path):
        os.system('killall ' + os.path.basename(path))
        time.sleep(2)
        os.system('rm -rf /tmp/*.info* /tmp/*.tmp*')
        os.system(path + ' &')
    else:
        print "ERROR! Cannot restart cccam! Restart manually or fix variable path cccamBin! Current value: " + path

#endregion
