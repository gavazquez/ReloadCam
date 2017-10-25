#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Cccamspot(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNXIz9DO16Ghp2KmsLqh2Nze1ZOYl6dis6m9')
        return realUrl

    def GetClines(self):
        print "Now getting Cccamspot clines!"
        cccamspotClines = []
        cccamspotClines.append(self.__GetCccamspotCline())
        cccamspotClines = filter(None, cccamspotClines)
        if len(cccamspotClines) == 0: print "No Cccamspot lines retrieved"
        return cccamspotClines

    def __GetCccamspotCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
