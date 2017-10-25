#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Kingcccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #'http://kyng.cccam.bz/top/cccam.php'
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfN3e2taPx5SVlKFxo8eh2dvfkMeUlZShcbG14g==')
        return realUrl

    def GetClines(self):
        print "Now getting Kingcccam clines!"
        kingcccamClines = []
        kingcccamClines.append(self.__GetKingcccamCline())
        kingcccamClines = filter(None, kingcccamClines)
        if len(kingcccamClines) == 0: print "No Kingcccam lines retrieved"
        return kingcccamClines

    def __GetKingcccamCline(self):

        values= {
            'User': ReloadCam_Helper.GetRandomString(5),
            'Pass': ReloadCam_Helper.GetRandomString(5),
            'cccam':''
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
