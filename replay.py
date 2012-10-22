# World Of Tanks replay file parser/clanwar filter.
# Copyright (C) 20120817 Rasz_pl
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For more information please view the readme file.
#

import sys
import binascii
import array
import time
import hashlib
import random
import string,os
import struct
import threading
import json
from pprint import pprint
from datetime import datetime
import os
import shutil
# most of those imports are redundand, im lazy like that


def custom_listdir(path):
# Returns the content of a directory by showing directories first
# and then files by ordering the names alphabetically

  dirs = sorted([d for d in os.listdir(path) if os.path.isdir(path + os.path.sep + d)])
  dirs.extend(sorted([f for f in os.listdir(path) if os.path.isfile(path + os.path.sep + f)]))

  return dirs


def main():

  file = "1"
  t1 = time.clock()

  for files in custom_listdir("."):
   if files.endswith(".wotreplay"):

     while True:
      processing = 0
      f = open(files, "rb")
      f.seek(4)

      if (struct.unpack("i",f.read(4))[0]==1): processing =1; f.close(); break

#      f.seek(0,2)
#      size = f.tell()
      f.seek(8)
      first_size = struct.unpack("i",f.read(4))
#      print (first_size[0], files)
      first_chunk = f.read(first_size[0])
      first_chunk_decoded = json.loads(first_chunk.decode('utf-8'))

      second_size = struct.unpack("i",f.read(4))
      second_chunk = f.read(second_size[0])
      second_chunk_decoded = json.loads(second_chunk.decode('utf-8'))

      f.close()

# dont remember what this commented out part did, probly used it during development :P
 #     pprint (first_chunk_decoded)
#     print (first_chunk.decode("utf-8"))

# list clantags of ur team 
 #     for a in first_chunk_decoded['vehicles']:
  #      print (first_chunk_decoded['vehicles'][a]['clanAbbrev'])


#      for a in first_chunk_decoded:

 #     pprint (first_chunk_decoded)
 #     print (first_chunk_decoded['playerID'])
#      print (first_chunk_decoded['vehicles'][first_chunk_decoded['playerID']])
#      print (" number of players: ",len(first_chunk_decoded['vehicles']))
      
#      count = len(first_chunk_decoded['vehicles'])
      #print ( first_chunk_decoded['vehicles'][first_chunk_decoded['vehicles'].keys()[0]] )


      if (len(first_chunk_decoded['vehicles'])==len(second_chunk_decoded[1])): processing =11; break


      first_tag = ""
      first_team = ""
      second_tag = ""

      for num in second_chunk_decoded[1]:
       a = second_chunk_decoded[1][num]
       if (first_tag == ""):
        first_tag = a['clanAbbrev']
        first_team = a['team']
       elif (a['team'] != first_team) and (a['clanAbbrev'] != first_tag) and (second_tag == ""):
        second_tag = a['clanAbbrev']
       elif (a['team'] == first_team) and (a['clanAbbrev'] != first_tag):
        processing =3
       elif (a['team'] != first_team) and (a['clanAbbrev'] == first_tag):
        processing =5
       elif (a['team'] != first_team) and (a['clanAbbrev'] != second_tag):
        processing =4

        
      if processing !=0: break


      if first_team != 1:
       first_tag, second_tag = second_tag, first_tag
      print ("CW between",first_tag,"and", second_tag)

      d = datetime.strptime(first_chunk_decoded['dateTime'], '%d.%m.%Y %H:%M:%S')
      d= d.strftime('%Y%m%d_%H%M')
      
      if second_chunk_decoded[0]['isWinner']==1: winlose="Win"
      else : winlose="Los"

      if not os.path.exists("clanwars"):
        os.makedirs("clanwars")

      print (files)
      first_tag = first_tag +"_"*(5-len(first_tag))
      second_tag = second_tag +"_"*(5-len(second_tag))
# You can change cw filename format here.
      newfile = "clanwars/"+"cw"+d+"_"+first_tag+"_"+second_tag+"_"+winlose+"_"+"-".join(first_chunk_decoded['playerVehicle'].split("-")[1:])+"_"+first_chunk_decoded['mapName']+".wotreplay"
      print (newfile)

# move or copy? too lazy to make it a command line parameter
#      shutil.copy2(files, newfile)
      shutil.move(files, newfile)

        
#      pprint (second_chunk_decoded[0])
      
      
  #    for a in first_chunk_decoded['vehicles']:
 #       clan = first_chunk_decoded['vehicles'][a]['clanAbbrev']
 #       if (struct.unpack("i",f.read(4))[0])==2: 


     #  print (first_chunk_decoded['gameplayType'])
#      for a in first_chunk_decoded:
 #      print (first_chunk_decoded['gameplayType'])
  #     print ([a])
      
 #      second_size = struct.unpack("i",f.read(4))
#      print (second_size[0], size, size-second_size[0]-first_size[0])

#     f.seek(second_size[0],0)
#       second_chunk = f.read(second_size[0])
  #     second_chunk_decoded = json.loads(second_chunk.decode('utf-8'))
       
 #      print (" number of players2 ",len(second_chunk_decoded))
 #      pprint (second_chunk_decoded)
#     print (second_chunk.decode("utf-8"))



 #     for a in second_chunk_decoded[1]:
  #     print (second_chunk_decoded[1][a]['clanAbbrev'])
    

      processing =10; break

     wazup = {
              0: 'Processing',
              1: 'incomplete replay',
              2: 'blah',
              3: 'same team clan mismatch',
              4: 'opposite team clan mismatch',
              5: 'same clan on both sides, WTF?',
              11: 'no fog of war = not a clanwar',
              10: ''
             }

#     print ()
#     print (files)

#     print (wazup[processing])

     if processing==1:
      if not os.path.exists("incomplete"):
       os.makedirs("incomplete")
# move or copy? too lazy to make it a command line parameter       
#      shutil.copy(files, "incomplete/"+files)
      shutil.move(files, "incomplete/"+files)

     if processing==11:
      if not os.path.exists("complete"):
       os.makedirs("complete")
# move or copy? too lazy to make it a command line parameter
#      shutil.copy(files, "complete/"+files)
      shutil.move(files, "complete/"+files)



  t2 = time.clock()
  print ()
  print  ("Shit took %0.3fms"  % ((t2-t1)*1000))


main()