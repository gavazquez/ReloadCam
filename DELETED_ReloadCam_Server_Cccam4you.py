#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 7

#Filename must start with Server, classname and argument must be the same!
class Cccam4you(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://cccam-free2.com/cccamfree/get.php
        if serverNo <= 1:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNXIz9DOkZekmJl1b7Dh0pvSxMeSn5mmqKZ82crgndHMoQ==')
        else:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453Ex5SToGi8sMKgyNvckMqjl5hocqiy5pPc19E=')

        return realUrl

    def GetClines(self):
        print "Now getting Cccam4you clines!"
        cccam4youClines = []
        cccam4youClines.append(self.__GetCccam4youCline(1))
        cccam4youClines.append(self.__GetCccam4youCline(2))
        cccam4youClines = filter(None, cccam4youClines)
        if len(cccam4youClines) == 0: print "No Cccam4you lines retrieved"
        return cccam4youClines

    def __GetCccam4youCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
