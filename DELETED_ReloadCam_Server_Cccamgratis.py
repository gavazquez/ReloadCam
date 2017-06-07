#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 3

#Filename must start with Server, classname and argument must be the same!
class Cccamgratis(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://cccam.gratis/1092/index.php
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNXIz9DOkpiklKistHzY19HUkM2flpiscbG14g==')
        return realUrl

    def GetClines(self):
        print "Now getting Cccamgratis clines!"
        camGratisClines = []
        camGratisClines.append(self.__GetCccamgratisCline())
        camGratisClines = filter(None, camGratisClines)
        if len(camGratisClines) == 0: print "No Cccamgratis lines retrieved"
        return camGratisClines

    def __GetCccamgratisCline(self):

        values= {
            'user': ReloadCam_Helper.GetRandomString(5),
            'pass': ReloadCam_Helper.GetRandomString(5),
            'submit':'Active User!',
        }

        header= {
            'Cookie': 'GenSession=cualquier+cosa',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, header, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
