#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Mycccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfOnc453O3ZSVlpWwc4GgyNvckN9hr6aqdXF-qJPc19E=")
        return realUrl

    def GetClines(self):
        print "Now getting Mycccam clines!"
        mycccamClines = []
        mycccamClines.append(self.__GetMycccamCline(1))
        mycccamClines.append(self.__GetMycccamCline(2))
        mycccamClines.append(self.__GetMycccamCline(3))
        mycccamClines.append(self.__GetMycccamCline(4))
        mycccamClines.append(self.__GetMycccamCline(5))
        mycccamClines.append(self.__GetMycccamCline(6))
        mycccamClines = filter(None, mycccamClines)
        if len(mycccamClines) == 0: print "No Mycccam lines retrieved"
        return mycccamClines

    def __GetMycccamCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl().format(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
