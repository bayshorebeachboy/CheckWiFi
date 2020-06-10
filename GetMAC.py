import string, os, datetime
from subprocess import call
from twilio.rest import Client
from datetime import datetime
import easygui
from easygui import *
#import urllib3
#urllib3.disable_warnings()
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# sms.py
# Sends sms message to any cell phone using gmail smtp gateway
# Written by Alex Le

import smtplib

# Use sms gateway provided by mobile carrier:
# at&t:     number@mms.att.net
# t-mobile: number@tmomail.net
# verizon:  number@vtext.com
# sprint:   number@page.nextel.com

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP( "smtp.gmail.com", 587 )

server.starttls()

server.login( 'xxxxxxxxx', 'xxxxxxxxxxx' )


#twillioSid = "AC81190e5d544d972d88ca6a3c1be682bf"
#twilioToken = "e3f010a1888995014ec92bf064f4c06c"
#twilioNumber = "+15413938714"
#myCell = "+"
#twilioCli = Client(twillioSid, twilioToken)
os.system("arp -a| grep -v 'incomplete' > /Users/Neal/Desktop/CheckWiFi/macs.out")

existings = open("/Users/Neal/Desktop/CheckWiFi/existing.txt").readlines()
acknowledged = False
now = str(datetime.now())


log = open('/Users/Neal/Desktop/CheckWiFi/log.txt', 'a')

node = []
for existing in existings:
    existing = existing.strip()
    node.append(existing)
    # print node
    
theLines = open("/Users/Neal/Desktop/CheckWiFi/macs.out")
for line in theLines:
    theLine = str(line)
    theMacs = theLine.split()
    theMac = str(theMacs[3]).strip("\n")
    theIP = str(theMacs[1]).strip("\n")
    print theIP
    #print theMacs[3]
    import sqlite3
    theConnection = sqlite3.connect('/Users/Neal/Library/Messages/chat.db')
    theCursor = theConnection.cursor()
    theCursor.execute("select text, date(date + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') as ddate from message where ddate = date('now', 'localtime') And text Like '%Un-known MAC Detected%'")
    if len(theCursor.fetchall()) > 0:
        acknowledged = True
        log.write(writeme)
    if theMac in node:
        print theMac, "Exists"
    else:
        # check to see if unknown node(s) have been acknowledged
        if acknowledged:
            print "Unknown Node ", theMac, " has been acknowledged"
        else:
            print 'Unknown MAC:IP ' + theMac + ':' + theIP + ' has been detected'
            writeme = 'Unknown MAC:IP ' + theMac + ':' + theIP + ' has been detected : ' + now + '\n'
            log.write(writeme)
            
            #message = twilioCli.messages.create(body="Unknown Node Detected" ,from_=twilioNumber, to=myCell)
            # Send text message through SMS gateway of destination number
            theMsg = 'Unknown MAC:IP ' + theMac + ':' + theIP + ' has been detected'
            print('The message is :', theMsg)
            server.sendmail( 'Check Wi-Fi', '5xxxxxxx@mms.att.net', 'Unknown MAC Detected')            
            #theMsg = 'Unknown MAC:IP ' + theMac + ':' + theIP + ' has been detected'
            msgbox(theMsg, "Scan Warning")
    
writeme = 'Ran at: ' + now + '\n'
log.write(writeme)
log.close
theLines.close
