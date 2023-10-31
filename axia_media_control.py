#!/usr/bin/python

import warnings
import Quartz

# telnetlib will be deprecated in Python 3.13, so we need to suppress the warning
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import telnetlib

PATHFINDER_IP = "192.168.20.11"
PATHFINDER_PORT = 93


# Connect to the telnet server
try:
    tn = telnetlib.Telnet(PATHFINDER_IP, PATHFINDER_PORT)
    print(f"Connection succeed to {PATHFINDER_IP}:{PATHFINDER_PORT}")
except:
    print("Connection error")
    exit(-1)

# Send the login and gpi watch messages
tn.write(b"LOGIN\r\n")
tn.write(b"ADD GPI 2\r\n")
# print the reply to the gpi watch message
print("Intial State: " + tn.read_until(b"\r\n").decode('ascii').split(" ")[2])


## Macos specific media key press code
# https://stackoverflow.com/questions/11045814/emulate-media-key-press-on-mac
# NSEvent.h
NSSystemDefined = 14
# hidsystem/ev_keymap.h
NX_KEYTYPE_PLAY = 16

def HIDPostAuxKey(key):
  def doKey(down):
    ev = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
      NSSystemDefined, # type
      (0,0), # location
      0xa00 if down else 0xb00, # flags
      0, # timestamp
      0, # window
      0, # ctx
      8, # subtype
      (key << 16) | ((0xa if down else 0xb) << 8), # data1
      -1 # data2
      )
    cev = ev.CGEvent()
    Quartz.CGEventPost(0, cev)
  doKey(True)
  doKey(False)

# Loop forever
while True:
    # match the GPI 2 Lhhhh or GPI 2 Hhhhh message
    tn.read_until(b"GPI 2 ")
    tn.read_until(b"\r\n")
    # press the media key play/pause button
    HIDPostAuxKey(NX_KEYTYPE_PLAY)