#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Seduct(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOXK0OTE2F-eopusr8Hhk9nUkNekrWOxcbG14g==')
        return realUrl

    def GetClines(self):
        print "Now getting Seduct clines!"
        myccclineClines = []
        myccclineClines.append(self.__GetSeductCline(1))
        myccclineClines.append(self.__GetSeductCline(2))
        myccclineClines.append(self.__GetSeductCline(3))
        myccclineClines.append(self.__GetSeductCline(4))
        return filter(None, myccclineClines)

    def __GetSeductCline(self, serverNo):

        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl().format(serverNo))
        cline = ReloadCam_Helper.FindClineInText(htmlCode, "([CN]:\s?\S+?\s+\d*\s+[0-9.]*\s?\w+)")

        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
