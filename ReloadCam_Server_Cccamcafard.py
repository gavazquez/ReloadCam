#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Cccamcafard(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNXIz9DOx5KYlKanb7Dh0pvgkdBipmmlc61-5pyb2M_IlqphpKux")
        return realUrl

    def GetClines(self):
        print "Now getting CCcamcafard clines!"
        cccamcafardClines = []
        cccamcafardClines.append(self.__GetCccamcafardCline())
        return filter(None, cccamcafardClines)

    def __GetCccamcafardCline(self):

        values= {
            'username': ReloadCam_Helper.GetRandomString(5),
            'add_user': ''
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
