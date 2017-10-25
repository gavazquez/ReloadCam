#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Bosscccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453D06SlYJempK7fk8_ezpOFl6aocbG14g==')
        return realUrl

    def GetClines(self):
        print "Now getting Bosscccam clines!"
        bosscccamClines = []
        bosscccamClines.append(self.__GetBosscccamCline())
        bosscccamClines = filter(None, bosscccamClines)
        if len(bosscccamClines) == 0: print "No Bosscccam lines retrieved"
        return bosscccamClines

    def __GetBosscccamCline(self):
        import re

        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)        
        if cline is None: 
            print 'Failed to obtain cline from html code of ' + self.GetUrl(serverNo)
            return None
        if ReloadCam_Helper.TestCline(cline):
            return cline
        return None
