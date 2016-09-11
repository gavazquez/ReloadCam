#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 8

#Filename must start with Server, classname and argument must be the same!
class Cccamcafard(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        if serverNo <= 1:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNnK2tTTxaWhpWKmpLDT0s_Qx8WjlmGXsq5815ji5JPMY2ZinbGlsuqT3NfR')
        else:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNnK2tTTxaWhpWKmpLDT0s_Qx8WjlmGXsq582pvTosSXlWZrY6yvsdfdmt_J1A==')

        return realUrl

    def GetClines(self):
        print "Now getting Cccamcafard clines!"
        cccamcafardClines = []
        cccamcafardClines.append(self.__GetCccamcafardCline(1))
        cccamcafardClines.append(self.__GetCccamcafardCline(2))
        cccamcafardClines = filter(None, cccamcafardClines)
        if len(cccamcafardClines) == 0: print "No CCcamcafard lines retrieved"
        return cccamcafardClines

    def __GetCccamcafardCline(self, serverNo):

        if serverNo <= 1:
            values= {
                'username': ReloadCam_Helper.GetRandomString(5),
                'add_user': ''
            }
        else:
            values= {
                'user': ReloadCam_Helper.GetMyIP(),
                'pass': 'cccamcafard.com'
            }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
