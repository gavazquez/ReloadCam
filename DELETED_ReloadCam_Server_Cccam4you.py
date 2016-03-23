#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Cccam4you(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNXIz9DOmKqhqGKmsLqhq760ppOYl6dis6m9")
        #http://cccam4you.com/FREE/get.php
        return realUrl

    def GetClines(self):
        print "Now getting Cccam4you clines!"
        cccam4youClines = []
        cccam4youClines.append(self.__GetCccam4youCline())
        cccam4youClines = filter(None, cccam4youClines)
        if len(cccam4youClines) == 0: print "No Cccam4you lines retrieved"
        return cccam4youClines

    def __GetCccam4youCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
