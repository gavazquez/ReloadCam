#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 1

#Filename must start with Server, classname and argument must be the same!
class Freecline(ReloadCam_Main.Server):

    def GetUrl(self):
        return None

    def GetClines(self):
        print "Now getting Freecline clines!"
        freeClineClines = []
        freeClineClines += self.__GetFreeclineClines()
        freeClineClines += self.__GetFreeclineNlines()
        return filter(None, freeClineClines)

    def __GetFreeclineClines(self):
        import re, time, datetime, random
        clines = []

        header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
        url = "http://www.freecline.com/history/CCcam/" + datetime.date.today().strftime("%Y/%m/%d")
        htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)

        regExpr = re.compile('Detailed information of the line.*([C]:.*?)<.*\n.*\n.*\n.*\n.*online')
        matches = regExpr.findall(htmlCode)

        while len(matches) < 3:
            yesterday = datetime.date.today() - datetime.timedelta( days = 1 )        
            url = "http://www.freecline.com/history/CCcam/" + yesterday.strftime("%Y/%m/%d")
            htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)
            matches = regExpr.findall(htmlCode)

        for i in range(0, 3):
            if ReloadCam_Helper.TestCline(matches[i]):
                clines.append(matches[i])

        return clines;

    def __GetFreeclineNlines(self):
        import re, time, datetime, random
        nlines = []

        header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
        url = "http://www.freecline.com/history/Newcamd/" + datetime.date.today().strftime("%Y/%m/%d")
        htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)

        regExpr = re.compile('Detailed information of the line.*([N]:.*?)<.*\n.*\n.*\n.*\n.*online')
        matches = regExpr.findall(htmlCode)

        while len(matches) < 3:
            yesterday = datetime.date.today() - datetime.timedelta( days = 1 )        
            url = "http://www.freecline.com/history/Newcamd/" + yesterday.strftime("%Y/%m/%d")
            htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)
            matches = regExpr.findall(htmlCode)

        for i in range(0, 3):
            if ReloadCam_Helper.TestCline(matches[i]):
                nlines.append(matches[i])

        return nlines;
