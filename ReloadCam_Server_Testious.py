#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Main, ReloadCam_Helper

def GetVersion():
    return 2

#Filename must start with Server, classname and argument must be the same!
class Testious(ReloadCam_Main.Server):

    def GetUrl(self):
        return None

    def GetClines(self):
        print "Now getting Testious clines!"
        testiousClines = filter(None, self.__GetTestiousClines())
        if len(testiousClines) == 0: print "No Testious lines retrieved"
        return testiousClines

    def __GetTestiousClines(self):
        import re, time, datetime

        clines = []

        header = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
        url = "http://www.testious.com/free-cccam-servers/" + datetime.date.today().strftime("%Y-%m-%d")
        htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)

        regExpr = re.compile('([CN]:.*?)#.*\n<br>')
        matches = regExpr.findall(htmlCode)

        while len(matches) < 5:
            yesterday = datetime.date.today() - datetime.timedelta( days = 1 )        
            url = "http://www.testious.com/free-cccam-servers/" + yesterday.strftime("%Y-%m-%d")
            htmlCode = ReloadCam_Helper.GetHtmlCode(header, url)
            matches = regExpr.findall(htmlCode)

        for i in range(0, 5):
            if ReloadCam_Helper.TestCline(matches[i]):
                clines.append(matches[i])

        return clines;
