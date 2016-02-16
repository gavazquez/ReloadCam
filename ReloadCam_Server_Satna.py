#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Satna(ReloadCam_Main.Server):
    
    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfOXG4N3CmJaomKZxr7yfztydw82rYaaVt6-uoeCc7NTWp2CjnLM=")
        return realUrl

    def GetClines(self):
        print "Now getting Satna clines!"
        satnaClines = []
        satnaClines.append(self.__GetSatnaCline(1))
        satnaClines.append(self.__GetSatnaCline(2))
        satnaClines.append(self.__GetSatnaCline(3))
        satnaClines.append(self.__GetSatnaCline(4))
        satnaClines.append(self.__GetSatnaCline(5))
        satnaClines.append(self.__GetSatnaCline(6))
        return filter(None, satnaClines)

    def __GetSatnaCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl().format(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
