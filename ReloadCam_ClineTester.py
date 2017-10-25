#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger - https://github.com/gavazquez

def GetVersion():
    return 5

recvblock = None
sendblock = None

def TestCline(cline, timeout):
    import socket, re, sys, array, time, select

    global recvblock
    recvblock = CryptographicBlock()

    global sendblock
    sendblock = CryptographicBlock()

    returnValue = False
    regExpr = re.compile('[C]:\s*(\S+)+\s+(\d*)\s+(\S+)\s+([\w./\-]+)')
    match = regExpr.search(cline)

    if match is None:
        return False;

    testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    testSocket.settimeout(timeout)

    host = match.group(1)
    port = int(match.group(2))
    username = match.group(3)
    password = match.group(4)

    try:
        ip = socket.gethostbyname(host)
        testSocket.connect((ip, port))

        __DoHanshake(testSocket)

        try:
            userArray = __GetPaddedUsername(username)
            sendcount = __SendMessage(userArray, len(userArray), testSocket)
            
            passwordArray = __GetPaddedPassword(password)
            sendblock.Encrypt(passwordArray, len(passwordArray))
    
            cccamArray = __GetCcam()
            sendcount = __SendMessage(cccamArray, len(cccamArray), testSocket)

            receivedBytes = bytearray(20)
            recvCount = testSocket.recv_into(receivedBytes, 20)

            if recvCount > 0:
                recvblock.Decrypt(receivedBytes, 20)
                if (receivedBytes.decode("ascii").rstrip('\0') == "CCcam"):
                    returnValue = True
        except:
            pass
    except:
        pass

    testSocket.close()
    return returnValue

def __GetPaddedUsername(userName):
    import array

    #We create an array of 20 bytes with the username in it as bytes and padded with 0 behind
    #Like: [23,33,64,13,0,0,0,0,0,0,0...]
    userBytes = array.array("B", userName)
    userByteArray = __FillArray(bytearray(20), userBytes)

    return userByteArray

def __GetCcam():
    import array

    #We create an array of 6 bytes with the "CCcam\0" in it as bytes
    cccamBytes = array.array("B", "CCcam") 
    cccamByteArray = __FillArray(bytearray(6), cccamBytes)
    return cccamByteArray

def __GetPaddedPassword(password):
    import array

    #We create an array of with the password in it as bytes
    #Like: [23,33,64,13,48,78,45]
    passwordBytes = array.array("B", password)
    passwordByteArray = __FillArray(bytearray(len(password)),passwordBytes)

    return passwordByteArray
    
def __DoHanshake(socket):
    import hashlib, array

    random = bytearray(16)
    socket.recv_into(random, 16) #Receive first 16 "Hello" random bytes

    random = __Xor(random); #Do a Xor with "CCcam" string to the hello bytes

    sha1 = hashlib.sha1()
    sha1.update(random)
    sha1digest = array.array('B', sha1.digest()) #Create a sha1 hash with the xor hello bytes
    sha1hash = __FillArray(bytearray(20), sha1digest)

    recvblock.Init(sha1hash, 20) #initialize the receive handler
    recvblock.Decrypt(random, 16)

    sendblock.Init(random, 16) #initialize the send handler
    sendblock.Decrypt(sha1hash, 20)

    rcount = __SendMessage(sha1hash, 20, socket) #Send the a crypted sha1hash!    
    
def __SendMessage(data, len, socket):
    buffer = __FillArray(bytearray(len), data)
    sendblock.Encrypt(buffer, len)
    rcount = socket.send(buffer)
    return rcount

def __FillArray(array, source):
    if len(source) <= len(array):
        for i in range(0, len(source)):
            array[i] = source[i]
    else:
        for i in range(0, len(array)):
            array[i] = source[i]
    return array

def __Xor(buf):
    cccam = "CCcam"
    for i in range(0, 8):
        buf[8 + i] = 0xff & (i * buf[i])
        if i < 5:   
            buf[i] ^= ord(cccam[i])
    return buf

#region CriptoBlock

class CryptographicBlock(object):
    def __init__(self):
        self._keytable = [0] * 256
        self._state = 0
        self._counter = 0
        self._sum = 0

    def Init(self, key, len):
        for i in range(0, 256):
            self._keytable[i] = i
        j = 0
        for i in range(0, 256):
            j = 0xff & (j + key[i % len] + self._keytable[i])
            self._keytable[i], self._keytable[j] = self._keytable[j], self._keytable[i]
        self._state = key[0]
        self._counter = 0
        self._sum = 0

    def Decrypt(self, data, len):
        for i in range(0, len):
            self._counter = 0xff & (self._counter + 1)
            self._sum = self._sum + self._keytable[self._counter]

            #Swap keytable[counter] with keytable[sum]
            self._keytable[self._counter], self._keytable[self._sum & 0xFF] = \
                self._keytable[self._sum & 0xFF], self._keytable[self._counter]

            z = data[i]
            data[i] = z ^ self._keytable[(self._keytable[self._counter] + \
                self._keytable[self._sum & 0xFF]) & 0xFF] ^ self._state
            z = data[i]
            self._state = 0xff & (self._state ^ z)

    def Encrypt(self, data, len):
        for i in range(0, len):
            self._counter = 0xff & (self._counter + 1)
            self._sum = self._sum + self._keytable[self._counter]
            
            #Swap keytable[counter] with keytable[sum]
            self._keytable[self._counter], self._keytable[self._sum & 0xFF] = \
                self._keytable[self._sum & 0xFF], self._keytable[self._counter]

            z = data[i]
            data[i] = z ^ self._keytable[(self._keytable[self._counter & 0xFF] + \
                self._keytable[self._sum & 0xFF]) & 0xff] ^ self._state

            self._state = 0xff & (self._state ^ z)

#endregion
