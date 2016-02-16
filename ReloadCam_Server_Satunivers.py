#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Satunivers(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfOXG4OTPzaeXpadxpbHg2Jrdxthgm6GYqLl74s3c")
        return realUrl

    def GetClines(self):
        print "Now getting Satunivers clines!"
        satUniverseClines = []
        satUniverseClines.append(self.__GetSatuniversCline())
        return filter(None, satUniverseClines)

    def __GetSatuniversCline(self):

        values= {
            'user': ReloadCam_Helper.GetRandomString(5),
            'pass': ReloadCam_Helper.GetRandomString(5)
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
