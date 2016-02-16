#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Mycccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfOnc453O3ZSVlpWwc4GgyNvckN9hr6aqdXF-qJPc19E=")
        return realUrl

    def GetClines(self):
        print "Now getting Myccam clines!"
        myccclineClines = []
        myccclineClines.append(self.__GetMycccamCline(1))
        myccclineClines.append(self.__GetMycccamCline(2))
        myccclineClines.append(self.__GetMycccamCline(3))
        myccclineClines.append(self.__GetMycccamCline(4))
        myccclineClines.append(self.__GetMycccamCline(5))
        myccclineClines.append(self.__GetMycccamCline(6))
        return filter(None, myccclineClines)

    def __GetMycccamCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl().format(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
