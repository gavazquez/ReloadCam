#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 3

#Filename must start with Server, classname and argument must be the same!
class Mario(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)

        if (serverNo <= 4):
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453OxaObopempK7fk-DakLGSpJyjco5-oQ==')
        elif (serverNo >= 5 and serverNo <= 8):
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453OxaObopempK7fk-DakLGSpJyjco5_oQ==')
        elif (serverNo >= 9):
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOnc453OxaObopempK7fk-DakLGSpJyjco6AoQ==')
        
        realUrl = realUrl + str(serverNo)
        return realUrl

    def GetClines(self):
        print "Now getting Mario clines!"
        marioClines = []
        marioClines.append(self.__GetMarioCline(1))
        marioClines.append(self.__GetMarioCline(2))
        marioClines.append(self.__GetMarioCline(3))
        marioClines.append(self.__GetMarioCline(4))
        marioClines.append(self.__GetMarioCline(5))
        marioClines.append(self.__GetMarioCline(6))
        marioClines.append(self.__GetMarioCline(7))
        marioClines.append(self.__GetMarioCline(8))
        marioClines.append(self.__GetMarioCline(9))
        marioClines.append(self.__GetMarioCline(10))
        marioClines.append(self.__GetMarioCline(11))
        marioClines.append(self.__GetMarioCline(12))
        marioClines = filter(None, marioClines)
        if len(marioClines) == 0: print "No Mario lines retrieved"
        return marioClines

    def __GetMarioCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
