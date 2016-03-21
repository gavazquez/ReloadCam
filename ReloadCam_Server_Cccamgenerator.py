#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 3

#Filename must start with Server, classname and argument must be the same!
class Cccamgenerator(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNXIz9DOy5agmKaktbzkk8_ezpOUlZaVsHC019ma38nU")
        return realUrl

    def GetClines(self):
        print "Now getting Cccamgenerator clines!"
        cccamFreeClines = []
        cccamFreeClines.append(self.__GetCccamfreeCline())
        return filter(None, cccamFreeClines)

    def __GetCccamfreeCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
