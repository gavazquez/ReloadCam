#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Bosscccam(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453D06SlYJempK7fk8_ezpOXpJiZtqa_6Mre4o_MpZ-f')
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

        escaped = r"Host:\s([\w\-\.]*).*\n.*Port:\s([\d]*).*\n.*User:\s([\w\-\.]*).*\n.*Password:\s([\w\-\.]*)"
        regExpr = re.compile(escaped)
        matches = regExpr.findall(htmlCode)
        
        if len(matches[0]) == 4:
            cline = 'C: ' + matches[0][0] + ' ' + matches[0][1] + ' ' + matches[0][2] + ' ' + matches[0][3]
            if ReloadCam_Helper.TestCline(cline):
                return cline
        return None
