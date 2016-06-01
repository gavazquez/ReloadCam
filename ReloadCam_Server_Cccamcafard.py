#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 5

#Filename must start with Server, classname and argument must be the same!
class Cccamcafard(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453IyZ-XpZW3sL-gyM_SwtGUk5mVtaV71dTZnsjOmZ6anqutgaKZnJ7K0pWXq2Kzqb0=')
        return realUrl

    def GetClines(self):
        print "Now getting CCcamcafard clines!"
        cccamcafardClines = []
        cccamcafardClines.append(self.__GetCccamcafardCline())
        cccamcafardClines = filter(None, cccamcafardClines)
        if len(cccamcafardClines) == 0: print "No Cccamcafard lines retrieved"
        return cccamcafardClines

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
