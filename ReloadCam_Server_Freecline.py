#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 7

#Filename must start with Server, classname and argument must be the same!
class Freecline(ReloadCam_Main.Server):

    def GetUrl(self):
        return None

    def GetClines(self):
        print "Now getting Freecline clines!"
        freeClineClines = []
        freeClineClines += self.__GetFreeclineClines()
        freeClineClines += self.__GetFreeclineNlines()
        freeClineClines = filter(None, freeClineClines)
        if len(freeClineClines) == 0: print "No Freecline lines retrieved"
        return freeClineClines

    def __GetFreeclineClines(self):
        import re, time, datetime, random
        clines = []

        header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
        url = "http://www.freecline.com/history/CCcam/" + (datetime.date.today() - datetime.timedelta( days = 1 )).strftime("%Y/%m/%d").replace('0', '')
        htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)

        regExpr = re.compile('Detailed information of the line.*([C]:.*?)<.*\n.*\n.*\n.*\n.*online')
        matches = regExpr.findall(htmlCode)

        while len(matches) < 3:
            yesterday = datetime.date.today() - datetime.timedelta( days = 2 )
            url = "http://www.freecline.com/history/CCcam/" + yesterday.strftime("%Y/%m/%d").replace('0', '')
            htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)
            matches = regExpr.findall(htmlCode)

        for match in matches:
            if ReloadCam_Helper.TestClineTimeout(match,5):
                clines.append(match)

        ReloadCam_Helper.SortClinesByPing(clines)

        return clines[:5]; #return only the best 5 clines

    def __GetFreeclineNlines(self):
        import re, time, datetime, random
        nlines = []

        header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
        url = "http://www.freecline.com/history/Newcamd/" + (datetime.date.today() - datetime.timedelta( days = 1 )).strftime("%Y/%m/%d").replace('0', '')
        htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)

        regExpr = re.compile('Detailed information of the line.*([N]:.*?)<.*\n.*\n.*\n.*\n.*online')
        matches = regExpr.findall(htmlCode)

        while len(matches) < 3:
            yesterday = datetime.date.today() - datetime.timedelta( days = 2 )        
            url = "http://www.freecline.com/history/Newcamd/" + yesterday.strftime("%Y/%m/%d").replace('0', '')
            htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)
            matches = regExpr.findall(htmlCode)

        for match in matches:
            if ReloadCam_Helper.TestClineTimeout(match,5):
                nlines.append(match)

        ReloadCam_Helper.SortClinesByPing(nlines)

        return nlines[:5]; #return only the best 5 nlines
