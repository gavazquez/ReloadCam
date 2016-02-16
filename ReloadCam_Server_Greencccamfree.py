#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Greencccamfree(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNnX0dTPx5SVlKGps7LXk9DTz9dfoJiocqiy4Mua38nU")
        return realUrl

    def GetClines(self):
        print "Now getting Greencccamfree clines!"
        greencccamfreeClines = []
        greencccamfreeClines.append(self.__GetGreenCCCamFreeCline())
        return filter(None, greencccamfreeClines)

    def __GetGreenCCCamFreeCline(self):

        password = ReloadCam_Helper.GetRandomString(5)
        values= {
            'u1': ReloadCam_Helper.GetMyIP(),
            'clav1': password,
            'arrob1':   ReloadCam_Helper.GetRandomString(5) + "@" + ReloadCam_Helper.GetRandomString(5) + ".com"
        }

        header= {
           'Referer': self.GetUrl()
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, header, self.GetUrl())
        cline = ReloadCam_Helper.FindClineInText(htmlCode, "([CN]:\s?\S+?\s+\d*)")

        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline + " " + ReloadCam_Helper.GetMyIP() + " " + password
        return None
