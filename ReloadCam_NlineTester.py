#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Refrescador automatico de clines
#Creado por Dagger

def GetVersion():
    return 1

def TestNline(nline, timeout):
    import socket, re, sys, array, time, select, ReloadCam_Md5, random, ReloadCam_Des

    returnValue = False
    regExpr = re.compile('[N]:\s*(\S+)+\s+(\d*)\s+(\S+)\s+([\w.-]+)((?:\s(?:\d\d)){14})')
    match = regExpr.search(nline)

    if match is None:
        return False;

    testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    testSocket.settimeout(timeout)

    host = match.group(1)
    port = int(match.group(2))
    username = match.group(3)
    password = match.group(4)
    configKey = __ParseConfigKey(match.group(5))
    
    try:
        ip = socket.gethostbyname(host)
        testSocket.connect((ip, port))

        helloBytes = bytearray(14)
        testSocket.recv_into(helloBytes, 14) #Receive first 14 "Hello" random bytes
        print "Hello bytes: " + helloBytes

        loginKey = __GetLoginKey(configKey, helloBytes);

        #CAUTION! Md5 hash must be done as in UNIX Crypt() function.
        #The one that I'm using I grabbed it from: 
        #https://code.activestate.com/recipes/325204-passwd-file-compatible-1-md5-crypt/
        passwordBytes = ReloadCam_Md5.md5crypt(password,"abcdefgh")

        loginMessage = []
        __Add10EmptyHeaderBytes(loginMessage) #Add 10 '0' bytes at beginning
                
        loginMessage.append(0xE0); #This is the login byte
        loginMessage.append(0);
        loginMessage.append(50); #No idea what this is

        loginMessage = loginMessage + array.array("B", username).tolist() #Add username as bytes
        loginMessage.append(0); #Add a "0" as separator
        loginMessage = loginMessage + array.array("B", passwordBytes).tolist() #Add md5 hashed password
        loginMessage.append(0); #Add a "0" as separator

        __AddFooterChecksum(loginMessage) #Add the checksum to the bottom

        iv = bytearray(random.getrandbits(8) for i in range(8)) # get a random IV    

        encryptedBuffer = __EncriptData(loginMessage, loginKey, iv) #encript in trippleDES

        encryptedBuffer = encryptedBuffer + [b for b in iv] #Append the IV to the message
    
        encriptedBuffer = __AddLengthHeader(encryptedBuffer); #Insert the 2 length bytes in the top

        rcount = testSocket.send(bytearray(encriptedBuffer));

        try:
            receivedBytes = bytearray(100)
            recvCount = testSocket.recv_into(receivedBytes, 100)

            if recvCount > 0:
                receivedBytes = [b for b in receivedBytes] #transform bytearray to list
                receivedBytes = receivedBytes[:recvCount] #Trim by removing trailing zeroes
                receivedBytes = receivedBytes[2:] #Remove first 2 sum bytes

                iv = bytearray(receivedBytes[len(receivedBytes)-8:len (receivedBytes)]) #Last 8 bytes are the IV
                
                decriptedBuffer = __DecriptData(receivedBytes, loginKey, iv) #decript the data

                decriptedBuffer = decriptedBuffer[10:] #Remove first 10 '0' bytes            

                if (decriptedBuffer[0] == 0xE1):#225 (0xE1) = ACK (acknowledge, all ok)
                    testSocket.close()
                    print "SUCCESS! working nline: " + nline
                    returnValue = True
                else:#226 (0xE2) = NACK (bad data)
                    print "Bad username/password for nline: " + nline
                    returnValue = False
            else:
                print "Failed to receive answer, check 14 byte config key for nline: " + nline
                returnValue = False

        except:
            raise Exception("Could not send data")
    except:
        print "Error while connecting to nline: " + nline

    testSocket.close()
    return returnValue

def __AddLengthHeader(data):
    newData = []
    newData.append((len(data) >> 8) & 0xff)
    newData.append(len(data) & 0xff)
    newData += data
    return newData

def __EncriptData(data, loginKey, iv):
    import ReloadCam_Des, array
    
    #Encript with tripleDES in CBC mode and with '\0' as padding
    loginKeyAsString = str(loginKey)
    ivAsString = str(iv)
    des = ReloadCam_Des.triple_des(loginKeyAsString, ReloadCam_Des.CBC, ivAsString, pad= '\0', padmode = ReloadCam_Des.PAD_NORMAL)

    dataAsString = ''.join([chr(c) for c in data])

    encriptedData = des.encrypt(dataAsString);
    return array.array("B", encriptedData).tolist()

def __DecriptData(data, loginKey, iv):
    import ReloadCam_Des, array

    #Decript with tripleDES in CBC mode and with '\0' as padding
    loginKeyAsString = str(loginKey)
    ivAsString = str(iv)

    des = ReloadCam_Des.triple_des(loginKeyAsString, ReloadCam_Des.CBC, ivAsString, pad= '\0', padmode = ReloadCam_Des.PAD_NORMAL)

    dataAsString = ''.join([chr(c) for c in data])

    decriptedData = des.decrypt(dataAsString);
    return array.array("B", decriptedData).tolist()

def __Add10EmptyHeaderBytes(data):
    for i in range(0, 10):
        data.append(0)

def __AddFooterChecksum(data):
    xorSum = 0;
    for i in range(0, len(data)):
        xorSum = (xorSum ^ data[i]) & 0xFF;
    data.append(xorSum)

def __ParseConfigKey(configKey):
    import array

    configKey = configKey.replace(' ', '')
    configKey = configKey.replace(',', '')
    configKey = configKey.replace(':', '')
    byteDesKey = bytearray(len(configKey)/2)
    arrayCounter = 0;
    for i in range(0, len(configKey)/2):
        #Encode the config key in base 16 as int because python does not have a byte type
        byteDesKey[i] = int(configKey[arrayCounter:arrayCounter+2].encode(),16)
        arrayCounter = arrayCounter + 2

    return byteDesKey

def __GetLoginKey(configKey, helloBytes):

    #The login key is a 16 byte key made by xor of hello bytes and config key
    xoredKey = bytearray(len(configKey))
    for i in range(0, len(configKey)):
        xoredKey[i] = (configKey[i] ^ helloBytes[i]) & 0xFF;

    loginKey = bytearray(16)    
    #Do the key spread from 14 bytes to 16 bytes as tripleDES needs
    loginKey[0] = (xoredKey[0] & 0xfe) & 0xFF
    loginKey[1] = ((xoredKey[0] << 7 | xoredKey[1] >> 1) & 0xfe) & 0xFF
    loginKey[2] = ((xoredKey[1] << 6 | xoredKey[2] >> 2) & 0xfe) & 0xFF
    loginKey[3] = ((xoredKey[2] << 5 | xoredKey[3] >> 3) & 0xfe) & 0xFF
    loginKey[4] = ((xoredKey[3] << 4 | xoredKey[4] >> 4) & 0xfe) & 0xFF
    loginKey[5] = ((xoredKey[4] << 3 | xoredKey[5] >> 5) & 0xfe) & 0xFF
    loginKey[6] = ((xoredKey[5] << 2 | xoredKey[6] >> 6) & 0xfe) & 0xFF
    loginKey[7] = (xoredKey[6] << 1) & 0xFF
    loginKey[8] = (xoredKey[7] & 0xfe) & 0xFF
    loginKey[9] = ((xoredKey[7] << 7 | xoredKey[8] >> 1) & 0xfe) & 0xFF
    loginKey[10] = ((xoredKey[8] << 6 | xoredKey[9] >> 2) & 0xfe) & 0xFF
    loginKey[11] = ((xoredKey[9] << 5 | xoredKey[10] >> 3) & 0xfe) & 0xFF
    loginKey[12] = ((xoredKey[10] << 4 | xoredKey[11] >> 4) & 0xfe) & 0xFF
    loginKey[13] = ((xoredKey[11] << 3 | xoredKey[12] >> 5) & 0xfe) & 0xFF
    loginKey[14] = ((xoredKey[12] << 2 | xoredKey[13] >> 6) & 0xfe) & 0xFF
    loginKey[15] = (xoredKey[13] << 1) & 0xFF             
    
    #Here we adjust the parity?
    for i in range(0, len(loginKey)):                
        loginKey[i] = (loginKey[i] & 0xfe |
            (loginKey[i] >> 1 ^ loginKey[i] >> 2 ^ loginKey[i] >> 3 ^ loginKey[i] >> 4 ^
            loginKey[i] >> 5 ^ loginKey[i] >> 6 ^ loginKey[i] >> 7 ^ 1) & 1) & 0xFF

    return loginKey