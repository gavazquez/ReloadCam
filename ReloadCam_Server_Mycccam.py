#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Mycccam(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #http://www.mycccam24.com/no1.php
        dictionary = {
            1:'maanpH1wfOnc453O3ZSVlpWwc4GgyNvckNKgY2Gkq7E=',
            2:'maanpH1wfOnc453O3ZSVlpWwc4GgyNvckNKgZGGkq7E=',
            3:'maanpH1wfOnc453O3ZSVlpWwc4GgyNvckNKgZWGkq7E=',
            4:'maanpH1wfOnc453O3ZSVlpWwc4GgyNvckNKgZmGkq7E=',
        }

        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt(dictionary[serverNo])
        return realUrl

    def GetClines(self):
        print "Now getting Mycccam clines!"
        mycccamClines = []
        mycccamClines.append(self.__GetMycccamCline(1))
        mycccamClines.append(self.__GetMycccamCline(2))
        mycccamClines.append(self.__GetMycccamCline(3))
        mycccamClines.append(self.__GetMycccamCline(4))
        mycccamClines = filter(None, mycccamClines)
        if len(mycccamClines) == 0: print "No Mycccam lines retrieved"
        return mycccamClines

    def __GetMycccamCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl(serverNo).format(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
