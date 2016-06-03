#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Hacksat(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOXZzeGPzJKVnmG2osGg1N7WkJxoZ6eZrLC8oc7a08bcX6KbpA==')
        return realUrl

    def GetClines(self):
        print "Now getting Hacksat clines!"
        hackSatClines = []
        hackSatClines.append(self.__GetHacksatCline())
        hackSatClines = filter(None, hackSatClines)
        if len(hackSatClines) == 0: print "No Hacksat lines retrieved"
        return hackSatClines

    def __GetHacksatCline(self):

        values= {
            'user': ReloadCam_Helper.GetMyIP(),
            'pass': 'hack-sat.net',
            'submit':'Active User!'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
