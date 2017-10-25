#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 7

#Filename must start with Server, classname and argument must be the same!
class Cccamgenerator(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNXIz9DOkZekmJl1b7Dh0pvV08mWZGKbqLV74s3c')
        return realUrl

    def GetClines(self):
        print "Now getting Cccamgenerator clines!"
        cccamgeneratorClines = []
        cccamgeneratorClines.append(self.__GetCccamgeneratorCline())
        cccamgeneratorClines = filter(None, cccamgeneratorClines)
        if len(cccamgeneratorClines) == 0: print "No Cccamgenerator lines retrieved"
        return cccamgeneratorClines

    def __GetCccamgeneratorCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
