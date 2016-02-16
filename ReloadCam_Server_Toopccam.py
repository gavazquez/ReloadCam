#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Toopccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfObU29-Px5SVlKFxo8ehyM_SwtFfopuk")
        return realUrl

    def GetClines(self):
        print "Now getting Toopccam clines!"
        toopCCcamClines = []
        toopCCcamClines.append(self.__GetToopccamCline())
        return filter(None, toopCCcamClines)

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
