#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 3

#Filename must start with Server, classname and argument must be the same!
class Elaissaoui(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNfRzdjU15KhqJ1xr7yfztydxNNfp55jq6Kw3djN45DNn5aYrHGxteI=")
        return realUrl

    def GetClines(self):
        print "Now getting Elaissaoui clines!"
        elaissaouiClines = []
        elaissaouiClines.append(self.__GetElaissaouiCline())
        elaissaouiClines = filter(None, elaissaouiClines)
        if len(elaissaouiClines) == 0: print "No Elaissaoui lines retrieved"
        return elaissaouiClines

    def __GetElaissaouiCline(self):

        values= {
            'user': ReloadCam_Helper.GetMyIP(),
            'pass': 'hack-sat.net',
            'submit':'Active User!'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
