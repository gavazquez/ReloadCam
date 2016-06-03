#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Fullmonsters(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://fullmonsters.zapto.org/cccam-gratuit/js/teste1.php
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNfRzdjU15KhqJ1xqa7V0JniwthfoaWbcqWy5djf4pmTmqCXmbtvvdrV')
        return realUrl

    def GetClines(self):
        print "Now getting Fullmonsters clines!"
        fullmonstersClines = []
        fullmonstersClines.append(self.__GetFullmonstersCline())
        fullmonstersClines = filter(None, fullmonstersClines)
        if len(elaissaouiClines) == 0: print "No Fullmonsters lines retrieved"
        return elaissaouiClines

    def __GetFullmonstersCline(self):

        values= {
            'name': ReloadCam_Helper.GetMyIP(),
            'surname': 'Click_On_Ads'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
