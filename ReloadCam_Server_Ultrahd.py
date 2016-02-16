#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Ultrahd(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        "http://ultrahd.no-ip.biz/tv/free.php?new&2"
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOfR4OHCzJVgoaNwqr2gx9XpkNinYZmmqKZ74s3crs_JqFhl')
        return realUrl

    def GetClines(self):
        print "Now getting Cccam4you clines!"
        ultraHdClines = []
        ultraHdClines.append(self.__GetUltraHdCline())
        return filter(None, ultraHdClines)

    def __GetUltraHdCline(self):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
