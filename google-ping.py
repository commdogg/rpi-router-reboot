#!/usr/bin/env python

import RPi.GPIO as GPIO
import subprocess
import time
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

DELAY_BETWEEN_PINGS = 1    # delay in seconds
DELAY_BETWEEN_TESTS = 120 # delay in seconds
# if you want to add more sites change line below like this. ["google.com" , "9.9.9.9"]
SITES = ["8.8.8.8"]

# issue Linux ping command to determine internet connection status
def ping(site):
  
  cmd = "/bin/ping -c 1 " + site
  try:
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
  except subprocess.CalledProcessError as e:
    return 0
  else:
    return 1

# ping the sites in the site list the specified number of times
# and return number of successful pings
def ping_sites(site_list, wait_time, times):
  successful_pings = 0
  attempted_pings = times * len(site_list)
  for t in range(0, times):
    for s in site_list:
      successful_pings += ping(s)
      time.sleep(wait_time)

  return successful_pings

# main loop: ping sites, wait, repeat
while True:
  success = ping_sites(SITES, DELAY_BETWEEN_PINGS, 5)
  now = datetime.datetime.now()
  comma = (",")
  end = (";")
  with open("/home/pi/googs-log.txt", "a+") as file_object:
    file_object.write("\n")
    file_object.write(now.strftime("%Y-%m-%d %H:%M:%S"))
    file_object.write(comma)
    file_object.write("Successful Pings")
    file_object.write(comma)
    file_object.write(str(success))
    file_object.write(comma)
    file_object.write("Waiting 2 minutes")
    file_object.write(end)
  # print (now.strftime("%Y-%m-%d %H:%M:%S")),(comma),"Successful Pings",(comma),(success),(end)
  # uncomment above to print to terminal window
  # when success = 0 switch your relays.
  if success == 0:
    with open("/home/pi/googs-log.txt", "a+") as file_object:
      file_object.write("\n")
      file_object.write(now.strftime("%Y-%m-%d %H:%M:%S"))
      file_object.write(comma)
      file_object.write("Resetting, waiting 5 minutes")
      file_object.write(end)
    GPIO.output(18, True)
    time.sleep(10)
    GPIO.output(18, False)
    time.sleep(300)
  else:
    time.sleep(DELAY_BETWEEN_TESTS)
