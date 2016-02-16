#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

import ReloadCam_Arguments

def GetVersion():
    return 1

cryptoKey = "1234CAMreload"

#We encript and decript the urls in case the admins looks for their code...
#Encriptamos las webs por si los administradores de esas webs se ponen a buscar su propio codigo...
#NO ES UNA ENCRIPTACION MUY SEGURA! Es un simple Vigenere
def Encrypt(key, clearText):
    import base64

    encriptedText = []

    for i in range(len(clearText)):
        keyChar = key[i % len(key)]
        encriptedChar = chr((ord(clearText[i]) + ord(keyChar)) % 256)
        encriptedText.append(encriptedChar)

    return base64.urlsafe_b64encode("".join(encriptedText))

#We encript and decript the urls in case the admins looks for their code...
#Encriptamos las webs por si los administradores de esas webs se ponen a buscar su propio codigo...
#NO ES UNA ENCRIPTACION MUY SEGURA! Es un simple Vigenere
def Decrypt(key, encriptedText):
    import base64

    decryptedText = []
    encriptedText = base64.urlsafe_b64decode(encriptedText)

    for i in range(len(encriptedText)):
        keyChar = key[i % len(key)]
        decryptedChar = chr((256 + ord(encriptedText[i]) - ord(keyChar)) % 256)
        decryptedText.append(decryptedChar)

    return "".join(decryptedText)

def GetMyIP():
    import urllib, re

    site = urllib.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address

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
        htmlCode = opener.open(url).read()
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

    response = urllib2.urlopen(req)
    try:
        response = urllib2.urlopen(req)
        htmlCode = response.read()
    except:
        print "Could not open website! (No internet connection or bad URL: " + url + ")"
        return '';

    return htmlCode;

def FindStandardClineInText(text):
    return FindClineInText(text, "([CN]:\s?\S+?\s+\d*\s+\w+\s?\w+)");

def FindClineInText(text, regex):
    import re

    regExpr = re.compile(regex)
    match = regExpr.search(text)

    if match is None:
        return None;

    cline = match.group(1)

    return cline;

def TestCline(cline):
    import socket, re, sys

    regExpr = re.compile('[CN]:\s?(\S+)?\s+(\d*)')
    match = regExpr.search(cline)

    if match is None:
        return False;

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        host = match.group(1)
        port = int(match.group(2))
        ip = socket.gethostbyname(host)
        s.connect((ip, port))
        return True
    except:
        s.close()
        return False

    return False

def SortClinesByPing(clines):
    clines_ping = []
    for cline in clines:
        clines_ping.append([cline, PingCline(cline)])

    clines_ping = sorted(clines_ping, key=lambda cline: cline[1])   # sort by ping
    return [x[0] for x in clines_ping]

def PingCline(cline):
    import re, socket

    if cline in GetCustomClines(): #custom lines must be always first!
        return 0;

    regExpr = re.compile('[CN]:\s?(\S+)?\s+(\d*)')
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
