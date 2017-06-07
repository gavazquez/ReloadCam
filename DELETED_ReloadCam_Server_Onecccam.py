#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Onecccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #COMPLEX http://onecccam.com/free_cccam_generator/
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOHT0dLEx5KfYZeyrnzZytrU08WdYZqZsaa_09nb4Y_UmaI=')
        return realUrl

    def GetClines(self):
        print "Now getting Onecccam clines!"
        onecccamClineClines = []
        onecccamClineClines.append(self.__GetOnecccamCline())
        onecccamClineClines = filter(None, onecccamClineClines)
        if len(onecccamClineClines) == 0: print "No Onecccam lines retrieved"
        return onecccamClineClines

    def __GetOnecccamCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
