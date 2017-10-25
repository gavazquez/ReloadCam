#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Madvengers(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://madvengers-cccam.com/verif.php
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfN_G0OXG0piXpadwpLDVxtmdxNOeYamZtaqzoNXU3w==')
        return realUrl

    def GetClines(self):
        print "Now getting Madvengers clines!"
        madvengersClines = []
        madvengersClines.append(self.__GetMadvengersCline())
        madvengersClines = filter(None, madvengersClines)
        if len(madvengersClines) == 0: print "No Madvengers lines retrieved"
        return madvengersClines

    def __GetMadvengersCline(self):

        values= {
            'user': ReloadCam_Helper.GetRandomString(5),
            'pass': ReloadCam_Helper.GetRandomString(5),
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        #cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        cline = "C: madvengers-cccam.com 20000 " + values['user'] + " " + values['pass']
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
