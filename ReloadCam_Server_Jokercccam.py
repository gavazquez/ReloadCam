#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Jokercccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNzU19TTx5SVlKFxrbzZztrj0JKel2KiqbOy15Tnn96SoZqj")
        return realUrl

    def GetClines(self):
        print "Now getting Jokercccam clines!"
        jokerClines = []
        jokerClines.append(self.__GetJokerCline(1))
        jokerClines.append(self.__GetJokerCline(2))
        jokerClines.append(self.__GetJokerCline(3))
        jokerClines.append(self.__GetJokerCline(4))
        jokerClines.append(self.__GetJokerCline(5))
        jokerClines.append(self.__GetJokerCline(6))
        return filter(None, jokerClines)

    def __GetJokerCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl().format(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
