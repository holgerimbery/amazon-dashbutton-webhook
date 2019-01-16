import datetime
import logging
from urllib.request import urlopen
import sys
import base64
import datetime
import time
import os


logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


# Constants
timespan_threshhold = 35
##########################################################
# baseurl for webhook

baseurl = 'http://192.168.1.98'
##########################################################

# Global vars
lastpress = {}

def arp_display(pkt):
  button = 'no-arp-op-1'
  if pkt.haslayer(ARP):
    if pkt[ARP].op == 1: #who-has (request)
#########################################################    
# button definition section
      if pkt[ARP].hwsrc == '38:f7:3d:b9:d3:8b':
        button = 'wohnzimmer'

      elif pkt[ARP].hwsrc == '38:f7:3d:25:e7:c6':
        button = 'bad'
#########################################################
      else:
        button = 'unknown'

  if button == 'no-arp-op-1':
    sys.stdout.write('.')
  elif button == 'strange-device':
    sys.stdout.write(',')
  elif button == 'unknown':
    sys.stdout.write(';')

  else: # A relevant button was pressed
    thistime = datetime.datetime.now()
    print ('')
    print (button, ' was pressed now at ', thistime)

    if button in lastpress:
      lasttime = lastpress[button]
      print (button, ' was pressed before at ', lasttime)
      timespan = thistime - lasttime
      print ('timespan = ', timespan.total_seconds())
      if timespan.total_seconds() > timespan_threshhold:
        trigger(button)
      else:
        print ('No further action because timespan is shorter than ', timespan_threshhold, ' seconds.')
    else:
      print (button, ' was never pressed before.')
      trigger (button)

    lastpress[button] = thistime

def trigger(button):
  print ('Making HTTP request for: ', button)

  url = baseurl +'/addons/red/' + button

  #request = urllib.Request(url)
  response = urlopen(url)
  #the_page = response.read()
  #print ('')
  #print ('Response: ')
  #print (the_page)
  #print ('')


print ('Waiting for an amazon dash button to register to the network ...')
print ('')

sniff(prn=arp_display, filter="arp", store=0, count=0)

if __name__ == "__main__":
  main()

# eof
