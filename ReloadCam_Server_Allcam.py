#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez
import ReloadCam_Main
import ReloadCam_Helper

def GetVersion():
    return 10

#Filename must start with Server, classname and argument must be the same!
class Allcam(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        dictionary = {
            1:'maanpLZ7fKHc4-aPxZ2elpemorqgyNvckMuWpmRmcbG14g==',
            2:'maanpLZ7fKHc4-aPxZ2elpemorqgyNvckMuWpmRncbG14g==',
            3:'maanpLZ7fKHc4-aPxZ2elpemorqgyNvckMuWpmRocbG14g==',
            4:'maanpLZ7fKHc4-aPxZ2elpemorqgyNvckMuWpmRpcbG14g==',
        }

        realUrl = ReloadCam_Helper.Decrypt(dictionary[serverNo])
        return realUrl

    def GetClines(self):
        print "Now getting Allcam clines!"
        allcamClines = []
        allcamClines.append(self.__GetAllcamCline(1))
        allcamClines.append(self.__GetAllcamCline(2))
        allcamClines.append(self.__GetAllcamCline(3))
        allcamClines.append(self.__GetAllcamCline(4))
        allcamClines = filter(None, allcamClines)

        if len(allcamClines) == 0: print "No Allcam lines retrieved"
        return allcamClines

    def __GetAllcamCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl(serverNo))
        htmlCode = ReloadCam_Helper.CleanHtml(htmlCode)
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline is None: 
            print 'Failed to obtain cline from html code of ' + self.GetUrl(serverNo)
            return None
        if ReloadCam_Helper.TestCline(cline):
            return cline
        return None
