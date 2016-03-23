#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class ManiaForall(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://maniaforall.no-ip.org/index.php
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfN_G2tjCyqCklKCvb7vhktXfj9OjmWKdsaWy6pPc19E=')
        return realUrl

    def GetClines(self):
        print "Now getting ManiaForall clines!"
        maniaForallClines = []
        maniaForallClines.append(self.__GetManiaForallCline())
        maniaForallClines = filter(None, maniaForallClines)
        if len(maniaForallClines) == 0: print "No ManiaForall lines retrieved"
        return maniaForallClines

    def __GetManiaForallCline(self):

        values= {
            'user': ReloadCam_Helper.GetRandomString(5),
            'pass': 'mania',
            'submit':'Active User!'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None

