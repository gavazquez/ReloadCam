#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Cccamgenerador(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNXIz9DOy5agmKakpbzkk8_ezpOYpJSorLR82crgoY_UmaI=')
        return realUrl

    def GetClines(self):
        print "Now getting Cccamgenerador clines!"
        cccamgeneradorClines = []
        cccamgeneradorClines.append(self.__GetCccamgeneradorCline())
        cccamgeneradorClines = filter(None, cccamgeneradorClines)
        if len(cccamgeneradorClines) == 0: print "No Cccamgenerador lines retrieved"
        return cccamgeneradorClines

    def __GetCccamgeneradorCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
