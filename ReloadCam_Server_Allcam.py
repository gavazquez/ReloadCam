#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 7

#Filename must start with Server, classname and argument must be the same!
class Allcam(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        if serverNo == 1:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453C0J2VlpekrnvV1NmeyMmlY2Gkq7E=')
        elif serverNo == 2:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453C0J2VlpekrnvV1NmeyMmlZGGkq7E=')

        return realUrl

    def GetClines(self):
        print "Now getting Allcam clines!"
        allcamClines = []
        allcamClines.append(self.__GetAllcamCline(1))
        allcamClines.append(self.__GetAllcamCline(2))
        allcamClines = filter(None, allcamClines)
        if len(allcamClines) == 0: print "No Allcam lines retrieved"
        return allcamClines

    def __GetAllcamCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
