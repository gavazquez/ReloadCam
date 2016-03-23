#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Myfree(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfN_e0uHGyV-VlpekrnvU35vdxttglZaXpK574s3c')
        return realUrl

    def GetClines(self):
        print "Now getting Myfree clines!"
        myfreeClines = []
        myfreeClines.append(self.__GetMyfreeCline())
        myfreeClines = filter(None, myfreeClines)
        if len(myfreeClines) == 0: print "No Myfree lines retrieved"
        return myfreeClines

    def __GetMyfreeCline(self):

        values= {
            'Username': ReloadCam_Helper.GetRandomString(5),
            'Password': ReloadCam_Helper.GetRandomString(5),
            'cline':''
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
