#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Cccamlux(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453Ex5SToKC4uXvV1Nmep9aWl2B3hqSu35Pc19E=')
        return realUrl

    def GetClines(self):
        print "Now getting Cccamlux clines!"
        cccamluxClines = []
        cccamluxClines.append(self.__GetCccamluxCline())
        cccamluxClines = filter(None, cccamluxClines)
        if len(cccamluxClines) == 0: print "No Cccamlux lines retrieved"
        return cccamluxClines

    def __GetCccamluxCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
