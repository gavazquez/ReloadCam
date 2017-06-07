#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Powerfull(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOLU49TTyqaen5empK7fk8_ezpOhoaqZtafC3tGb1sbYX6KbpA==')
        return realUrl

    def GetClines(self):
        print "Now getting Powerfull clines!"
        powerfullClines = []
        powerfullClines.append(self.__GetPowerfullCline())
        powerfullClines = filter(None, powerfullClines)
        if len(powerfullClines) == 0: print "No Powerfull lines retrieved"
        return powerfullClines

    def __GetPowerfullCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
