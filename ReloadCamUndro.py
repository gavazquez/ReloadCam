#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#ReloadCamUndro creado por Zurder

def ReloadCamUndro():
   import ReloadCam, os
   # Read in the file
   with open(ReloadCam.cccamPath, 'r') as file :
      
      # Replace the target string 
      lines = [( '' + line.replace('C: ', 'C:').replace('|1|0', '').replace('DEFAULT:1', '#').replace('DEFAULT:0', '#').replace(' ', '|').rstrip('\n') + '|1|0' + "\n" ) for line in open(ReloadCam.cccamPath) ]

   # Write the file out again
   with open(ReloadCam.cccamPath, 'w') as file: 
   
      #IKS
      if lines == 0:
         file.write('DEFAULT:1\n')
      #CCCAM
      file.writelines(lines)


   import time
   # Reinicio de Spring.apk (al salir de qpython cargará de nuevo listas, canales, ...)
   os.system("adb shell am force-stop com.dvb.spring.home")
   
   print "Saliendo ..."
   
   # Salimos de qpython
   time.sleep(1.5)
   os.system("adb shell am force-stop com.hipipal.qpyplus")
