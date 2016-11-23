#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Bilalon(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNTO2NDN059goK25scCg2eKeydienmJ3hqSu35TV3cXJqWCjnLM=')
        return realUrl

    def GetClines(self):
        print "Now getting Bilalon clines!"
        bilalonClines = []
        bilalonClines.append(self.__GetBilalonCline())
        bilalonClines = filter(None, bilalonClines)
        if len(bilalonClines) == 0: print "No Bilalon lines retrieved"
        return bilalonClines

    def __GetBilalonCline(self):

        values= {
            'Username': ReloadCam_Helper.GetRandomString(5),
            'Password': ReloadCam_Helper.GetRandomString(5),
            'addf':''
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
