#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Top2servers(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNjX0dSWkqWho2a2pr_oyt7ij9inYZmmqKZ6tajP0M6TYmCjnLM=')
        return realUrl

    def GetClines(self):
        print "Now getting Top2servers clines!"
        top2Clines = []
        top2Clines.append(self.__GetTop2serversCline())
        return filter(None, top2Clines)

    def __GetTop2serversCline(self):

        values= {
            'user': ReloadCam_Helper.GetMyIP(),
            'email': ReloadCam_Helper.GetRandomString(4) + "@" + ReloadCam_Helper.GetRandomString(4) + ".com",
            'pass': ReloadCam_Helper.GetRandomString(5),
            'submit':'Activate!'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None

