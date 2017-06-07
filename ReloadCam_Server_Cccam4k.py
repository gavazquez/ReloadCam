#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Cccam4k(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)        
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNXIz9DO16Ghp2KmsLqh2Nze1ZOYl6dis6m9')
        return realUrl

    def GetClines(self):
        print "Now getting Cccam4k clines!"
        cccam4kClines = []
        cccam4kClines.append(self.__GetCccam4kCline())
        cccam4kClines = filter(None, cccam4kClines)
        if len(cccam4kClines) == 0: print "No Cccam4k lines retrieved"
        return cccam4kClines

    def __GetCccam4kCline(self):

        header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]

        htmlCode = ReloadCam_Helper.GetHtmlCode(header, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
