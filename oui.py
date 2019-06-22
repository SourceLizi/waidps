#!/usr/bin/python 
# -*- coding: utf-8 -*-

import os
import re
import struct
import sys
import time
import urllib.request

M_OUI_TYPE=3
#by defult it will download the lagest oui

def download_oui(oui_type):
    if oui_type == 1:# we will download MAC Address Block Small 
        DOWNLOAD="http://standards-oui.ieee.org/oui36/oui36.txt"
    elif oui_type == 2: #we will download MAC Address Block Medium
        DOWNLOAD="http://standards-oui.ieee.org/oui28/mam.txt"
    elif oui_type == 3: # we will download MAC Address Block Large
        DOWNLOAD="http://standards-oui.ieee.org/oui/oui.txt"
    else: return
    print("Start to download oui.txt ")
    urllib.request.urlretrieve(DOWNLOAD, "oui.txt",callback_report)
    print("   done")
pass

def callback_report(block_num,block_size,total):
    downloaded = block_num*block_size/total
    num = int(downloaded * 20)  # to show how many blocks  in progressbar to display
    #here  we set the maximum number of blocks to 20 
    sys.stdout.write("\r[%s%s]  %.1f%%" % ('█' *num , ' ' * (20-num),downloaded*100))
    sys.stdout.flush()
pass

    

def reformat_file():
    #read data from orginal oui.txt
    print("Reformating...")
    line=0
    list =[]
    try:
        f = open("oui.txt", 'r')
        while True:
            l = f.readline()
            if l == '': # end
                break
            line += 1
            l = l.strip('\n') # not need \n
            #print("#%d %s" % (line, l))
            ret = re.findall(r"^[A-F0-9].[A-F0-9].[A-F0-9].+$", l) # eg 9C8E99
            if len(ret) != 0:
                mac = l[:6]
                #mac_int = int(mac, 16) # string to int number
                org = l[22:]
                org.strip()
                test = mac+" "+org
                list.append(test) # add to list
        list.sort()
        f.close()
 
    except:
        raise
    line = 0
    #write mac-oui.db
    try:
        f2 = open("mac-oui.db", "w")
        f2.write("MAC Vendor - Updated "+str(time.strftime("%Y/%m/%d", time.localtime())) + "\n")
        for i in range(0, len(list)):
            #print("%d %s" % (i, list[i]))
            line += 1
            mac = list[i][:6]
            org = list[i][7:]
            #For debug:
            #mac_int = int(mac, 16) # string to int number
            #format='%ds' % len(org) # how many bytes in org
            #org_byte = struct.pack(format,str.encode(org))
            #org_len = len(org)
            #byte=struct.pack('i',mac_int) + struct.pack('b',org_len) + struct.pack(format,str.encode(org)) # to byte
            #print("333#%d 0x%x %d-->%s %s" % (i, mac_int, mac_int, org, org_byte))
            text = mac + " " + org + "\n"
            f2.write(text) 
 
        #some special mac address should be added
        f2.write("FFFF00400001 Lantastic \nFFFF00600004 Lantastic \nFFFF01E00004 Lantastic \nFFFFFF Broadcast \nFFFFFFFFFFFF Broadcast ") 
        f2.close()
        print("done. total number of data was %d,mac-oui.db was generated " % (line))
    except:
        raise
 
if __name__ == '__main__': 
    download_oui(M_OUI_TYPE)
    reformat_file()