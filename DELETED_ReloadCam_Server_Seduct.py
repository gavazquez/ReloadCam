#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 4

#Filename must start with Server, classname and argument must be the same!
class Seduct(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://seduct.loginto.me
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOXK0OTE2F-eopusr8Hhk9nUkNeWlq5kwG-92tU=')
        return realUrl

    def GetClines(self):
        print "Now getting Seduct clines!"
        seductClines = []
        seductClines.append(self.__GetSeductCline(1))
        seductClines.append(self.__GetSeductCline(2))
        seductClines.append(self.__GetSeductCline(3))
        seductClines.append(self.__GetSeductCline(4))   
        seductClines = filter(None, seductClines)
        if len(seductClines) == 0: print "No Seduct lines retrieved"
        return seductClines

    def __GetSeductCline(self, serverNo):

        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl().format(serverNo))
        cline = ReloadCam_Helper.FindClineInText(htmlCode, "([CN]:\s?\S+?\s+\d*\s+[0-9.]*\s?\w+)")

        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
