#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Hacksat(ReloadCam_Main.Server):

    def GetUrl(self, serverNo):
        #Pon un breakpoint aqui si quieres ver la URL verdadera ;)
        #'http://06.hack-sat.org/bg_j/index.php'
        #'http://star.hack-sat.org/yu_u/index.php'
        #'http://b1.hack-sat.org/l-01/index.php'
        if serverNo == 0:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfKKbmtfCx5xfppW3b7zkzJvRyMObYZyip6bFoNXU3w==')
        elif serverNo == 1: 
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfOXZzeGPzJKVnmG2osGg1N7WkN2mkahjrK-x192a38nU')
        else:
            realUrl = ReloadCam_Helper.Decrypt('maanpH1wfNSWmtfCx5xfppW3b7zkzJvbjpRiYZyip6bFoNXU3w==')
        return realUrl

    def GetClines(self):
        print "Now getting Hacksat clines!"
        hackSatClines = []
        hackSatClines.append(self.__GetHacksatCline(0))
        hackSatClines.append(self.__GetHacksatCline(1))
        hackSatClines.append(self.__GetHacksatCline(2))
        hackSatClines = filter(None, hackSatClines)
        if len(hackSatClines) == 0: print "No Hacksat lines retrieved"
        return hackSatClines

    def __GetHacksatCline(self, serverNo):

        values= {
            'user': ReloadCam_Helper.GetMyIP(),
            'pass': 'hack-sat.net',
            'submit':'Active User!'
        }

        htmlCode = ReloadCam_Helper.GetPostHtmlCode(values, None, self.GetUrl(serverNo))
        cline = ReloadCam_Helper.FindStandardClineInText(htmlCode)
        if cline != None and ReloadCam_Helper.TestCline(cline):
            return cline
        return None
