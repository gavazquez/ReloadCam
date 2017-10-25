#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 4

#Filename must start with Server, classname and argument must be the same!
class Toopccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #'http://plus.multics.tv/kk/cccam.php'
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOLR4eKP0aaep52mtHvm25vazJOUlZaVsG-92tU=')
        return realUrl

    def GetClines(self):
        print "Now getting Toopccam clines!"
        toopCCcamClines = []
        toopCCcamClines.append(self.__GetToopccamCline())
        top2Clines = filter(None, toopCCcamClines)
        if len(toopCCcamClines) == 0: print "No Toopccam lines retrieved"
        return toopCCcamClines

    def __GetToopccamCline(self):

        values= {
            'Username': ReloadCam_Helper.GetRandomString(5),
            'Password': ReloadCam_Helper.GetRandomString(5),
            'cline':'Order+New+CCCam'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
