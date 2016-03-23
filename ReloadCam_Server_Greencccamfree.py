#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 4

#Filename must start with Server, classname and argument must be the same!
class Greencccamfree(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)

        if serverNo == 0:
            realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNnX0dTPx5SVlKGps7LXk9DTz9dfoJiocqiy4Mua38nU")
        else: 
            realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNnX0dTPx5SVlKGps7LXk9DTz9dfoJiocqiy4MuendHMoQ==")

        return realUrl

    def GetClines(self):
        print "Now getting Greencccamfree clines!"
        greencccamfreeClines = []
        greencccamfreeClines.append(self.__GetGreenCCCamFreeCline(0))
        greencccamfreeClines.append(self.__GetGreenCCCamFreeCline(1))
        greencccamfreeClines = filter(None, greencccamfreeClines)
        if len(greencccamfreeClines) == 0: print "No Greencccamfree lines retrieved"
        return greencccamfreeClines

    def __GetGreenCCCamFreeCline(self, serverNo):
        ip = ReloadCam_Helper.GetMyIP()
        password = ReloadCam_Helper.GetRandomString(5)
        values= {
            'u1': ip,
            'clav1': password,
            'arrob1':   ReloadCam_Helper.GetRandomString(5) + "@" + ReloadCam_Helper.GetRandomString(5) + ".com"
        }

        header= {
           'Referer': self.GetUrl(serverNo)
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, header, self.GetUrl(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)

        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline + " " + ip + " " + password
        return None
