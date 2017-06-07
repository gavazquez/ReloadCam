#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Arguments

def GetVersion():
    return 22

cryptoKey = "1234CAMreload"
currentIpAddress = "0"

#Encriptamos las webs por si los administradores de esas webs se ponen a buscar su propio codigo...
#NO ES UNA ENCRIPTACION MUY SEGURA! Es un simple Vigenere
def Encrypt(clearText):
    import base64

    encriptedText = []

    for i in range(len(clearText)):
        keyChar = cryptoKey[i % len(cryptoKey)]
        encriptedChar = chr((ord(clearText[i]) + ord(keyChar)) % 256)
        encriptedText.append(encriptedChar)

    return base64.urlsafe_b64encode("".join(encriptedText))

#Encriptamos las webs por si los administradores de esas webs se ponen a buscar su propio codigo...
#NO ES UNA ENCRIPTACION MUY SEGURA! Es un simple Vigenere
def Decrypt(encriptedText):
    import base64

    decryptedText = []
    encriptedText = base64.urlsafe_b64decode(encriptedText)

    for i in range(len(encriptedText)):
        keyChar = cryptoKey[i % len(cryptoKey)]
        decryptedChar = chr((256 + ord(encriptedText[i]) - ord(keyChar)) % 256)
        decryptedText.append(decryptedChar)

    return "".join(decryptedText)

def GetMyIP():
    import urllib2, re

    global currentIpAddress

    if currentIpAddress == '0':
        currentIpAddress = TryGetIpAddress("http://ip.42.pl/raw", '(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})', 5)
    if currentIpAddress == '0':
        currentIpAddress = TryGetIpAddress("http://jsonip.com", '(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})', 5)
    if currentIpAddress == '0':
        currentIpAddress = TryGetIpAddress("http://ip.jsontest.com/", '([0-9.]*)', 5)
    if currentIpAddress == '0':
        currentIpAddress = TryGetIpAddress("http://httpbin.org/ip", '(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})', 5)
    if currentIpAddress == '0':
        currentIpAddress = TryGetIpAddress("https://api.ipify.org/", '(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})', 5)
    if currentIpAddress == '0':
        currentIpAddress = TryGetIpAddress("http://checkip.dyndns.org", '(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})', 15)

    return currentIpAddress

def TryGetIpAddress(url, regex, timeout):
    import urllib2, re

    try:
        return re.search(regex, urllib2.urlopen(url, timeout=5).read()).group(1)
    except:
        return ""
    

def GetRandomString(length):
    import random, string
    return ''.join(random.choice(string.lowercase) for i in range(length))

def GetHtmlCode(headers, url):
    import urllib, urllib2, cookielib

    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    if headers is not None and len(headers) > 0:
        opener.addheaders = headers
    try:
        htmlCode = opener.open(url, timeout=5).read()
        if htmlCode == '': raise Exception('No HTMLCode')
    except:
        print "Could not open website! (No internet connection or bad URL: " + url + ")"
        return '';

    return htmlCode;

def GetPostHtmlCode(data, headers, url):
    import urllib, urllib2, cookielib

    encodedData = urllib.urlencode(data)

    # Send HTTP POST request
    req = urllib2.Request(url, encodedData)

    if headers is not None:
        for key in headers.keys():
            req.add_header(key, headers[key])

    try:
        response = urllib2.urlopen(req, timeout=5)
        htmlCode = response.read()
        if htmlCode == '': raise Exception('No HTMLCode')
    except:
        print "Could not open website! (No internet connection or bad URL: " + url + ")"
        return '';

    return htmlCode;

def FindStandardClineInText(text):
    return FindClineInText(text, "([CN]:\s*\S+\s+\d+\s+\S+\s+[\w./\-]+)");



def CleanHtml(raw_html):
    import re
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def FindClineInText(text, regex):
    import re

    regExpr = re.compile(regex)
    match = regExpr.search(text)

    if match is None:
        return None;

    cline = match.group(1)

    return cline;

def TestCline(cline):
    if PingCline(cline) == 9999: 
        print "Cline: '" + cline + "' did not pass validation. (No ping)"
        return False
    clineValid = TestClineTimeout(cline, 15)
    if clineValid is False:
        print "Cline: '" + cline + "' did not pass validation. (user/pass invalid or timeout)"
    return clineValid

def TestClineTimeout(cline, timeout):
    import socket, re, sys, ReloadCam_ClineTester, ReloadCam_NlineTester

    regExpr = re.compile('[C].*')
    match = regExpr.search(cline)

    if match is None:
        regExpr = re.compile('[N].*')
        match = regExpr.search(cline)
        if match is not None:
            return ReloadCam_NlineTester.TestNline(cline,timeout)
        return False
    else:
        return ReloadCam_ClineTester.TestCline(cline,timeout)

def SortClinesByPing(clines):
    clines_ping = []
    for cline in clines:
        clines_ping.append([cline, PingCline(cline)])

    clines_ping = sorted(clines_ping, key=lambda cline: cline[1])   # sort by ping
    return [x[0] for x in clines_ping]

def PingCline(cline):
    import re, socket

    regExpr = re.compile('[CN]:\s+(\S+)+\s+(\d*)')
    match = regExpr.search(cline)

    if match is None:
        return 9999;

    try:
        ip = socket.gethostbyname(match.group(1))
        return Ping(ip)
    except:
        return 9999;

def Ping(host):
    import subprocess,platform,os,re

    ping = subprocess.Popen(
        ["ping", "-n" if  platform.system().lower()=="windows" else "-c", "1", host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    out, error = ping.communicate()

    if error is None or error == "":
        regExpr = re.compile('time=(\d+\.?\d*)')
        match = regExpr.search(out)
        if match is None:
            return 9999;
        return match.group(1)
    return 9999;
