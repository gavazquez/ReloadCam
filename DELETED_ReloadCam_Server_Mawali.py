#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Mawali(ReloadCam_Main.Server):

    def GetUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://mawali.no-ip.org/index.php
        realUrl = ReloadCam_Helper.Decrypt('maanpH1wfN_G49DNzV-gomGssXvh19OeytKVl6tis6m9')
        return realUrl

    def GetRedirectUrl(self):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt("maanpH1wfNfRzdjU15KhqJ1xr7yfztydxNNfp55j")
        return realUrl

    def GetClines(self):
        print "Now getting Mawali clines!"
        mawaliClines = []
        mawaliClines.append(self.__GetMawaliCline())
        mawaliClines = filter(None, mawaliClines)
        if len(mawaliClines) == 0: print "No Mawali lines retrieved"
        return mawaliClines

    def __GetMawaliCline(self):

        values= {
            'user': ReloadCam_Helper.GetRandomString(5),
            'pass': 'mawali',
            'submit':'Active+User!'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl())
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None

