#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Foot4sport(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://foot4sport.no-ip.org/index.php
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNjU2-OV16Ghpahxr7yfztyd0NaYYZyip6bFoNXU3w==')
        return realUrl

    def GetClines(self):
        print "Now getting Foot4sport clines!"
        foot4SportClines = []
        foot4SportClines.append(self.__GetFoot4sportCline())
        foot4SportClines = filter(None, foot4SportClines)
        if len(foot4SportClines) == 0: print "No Foot4sport lines retrieved"
        return foot4SportClines

    def __GetFoot4sportCline(self):

        values= {
            'user': ReloadCam_Helper.GetRandomString(5),
            'pass': 'foot',
            'submit':'Active User!'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None

