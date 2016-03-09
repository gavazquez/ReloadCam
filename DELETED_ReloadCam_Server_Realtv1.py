#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Realtv1(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfOTKzduO2KdjYZeyrnzoyt7Yx5KhmqM=")
        return realUrl

    def GetClines(self):
        print "Now getting Realtv1 clines!"
        realtv1Clines = []
        realtv1Clines.append(self.__GetRealtv1Cline())
        return filter(None, realtv1Clines)

    def __GetRealtv1Cline(self):

        values= {
            'user': ReloadCam_Helper.GetRandomString(5),
            'pass': ReloadCam_Helper.GetRandomString(5)
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
