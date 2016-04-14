#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 3

#Filename must start with Server, classname and argument must be the same!
class Jokercccam(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):

        dictionary = {
            1:'maanpH1wfNzU19TTx5SVlKFxrbzZztrj0JKel2KiqbOy15StoLupX6KbpA==',
            2:'maanpH1wfNzU19TTx5SVlKFxrbzZztrj0JKel2KiqbOy15StyZOpdWCjnLM=',
            3:'maanpH1wfNzU19TTx5SVlKFxrbzZztrj0JKel2KiqbOy15SytpSsX6KbpA==',
            4:'maanpH1wfNzU19TTx5SVlKFxrbzZztrj0JKel2KiqbOy15SttqmYX6KbpA==',
            5:'maanpH1wfNzU19TTx5SVlKFxrbzZztrj0JKel2KiqbOy15StwLiZX6KbpA==',
            6:'maanpH1wfNzU19TTx5SVlKFxrbzZztrj0JKel2KiqbOy15StpaOyX6KbpA=='
        }

        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        realUrl = ReloadCam_Helper.Decrypt(dictionary[serverNo])
        return realUrl

    def GetClines(self):
        print "Now getting Jokercccam clines!"
        jokerClines = []
        jokerClines.append(self.__GetJokerCline(1))
        jokerClines.append(self.__GetJokerCline(2))
        jokerClines.append(self.__GetJokerCline(3))
        jokerClines.append(self.__GetJokerCline(4))
        jokerClines.append(self.__GetJokerCline(5))
        jokerClines.append(self.__GetJokerCline(6))
        jokerClines = filter(None, jokerClines)
        if len(jokerClines) == 0: print "No Jokercccam lines retrieved"
        return jokerClines

    def __GetJokerCline(self, serverNo):
        htmlCode = ReloadCam_Helper.GetHtmlCode(None, self.GetUrl(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
