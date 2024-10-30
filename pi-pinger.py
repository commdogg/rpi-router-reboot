#!/usr/bin/env python

import RPi.GPIO as GPIO
import subprocess
import time
import datetime
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

DELAY_BETWEEN_PINGS = 2    # delay in seconds
DELAY_BETWEEN_TESTS = 120 # delay in seconds
NUMBER_OF_PINGS = 5 # How many Pings
SITES = ["8.8.8.8"] # if you want to add more sites change line below like this. ["google.com" , "9.9.9.9"]
HOMEDIR = os.getenv('HOME') # reads bash env variable for home directory
LOGFILE = "google-ping-log.txt" # sets logfile name
LOGPATH = os.path.join(HOMEDIR, LOGFILE) # creates path for logging commands
LATTHRESH = 60 #Acceptable Latency Threshold in milliseconds 
PINGTHRESH = 3 #Number of pings that must be successful per test

# function to issue Linux ping command to determine internet connection status
def ping(site):
  cmd = "/bin/ping -c 1 " + site
  try:
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
  except subprocess.CalledProcessError as e:
    return 0
  else:
    return 1

# function to grab rtt avg metrics from a series of 5 pings, icmp latency
def latency(site):
  stringlit = "'{print $4}'"
  command = f"/bin/ping -c 5 {site} | tail -1| awk {stringlit} | cut -d '/' -f 2"
  output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
  return float(output)
  
# function to ping the sites in the site list the specified number of times and return number of successful pings
def ping_sites(site_list, wait_time, times):
  successful_pings = 0
  attempted_pings = times * len(site_list)
  for t in range(0, times):
    for s in site_list:
      successful_pings += ping(s)
      time.sleep(wait_time)
  return successful_pings

# latency check against site list
def lat_sites(site_list):
  rtt = 0
  len(site_list)
  for s in site_list:
      rtt += latency(s)
  return rtt

# main loop: ping sites, wait, repeat
while True:
  success = ping_sites(SITES, DELAY_BETWEEN_PINGS, NUMBER_OF_PINGS)
  now = datetime.datetime.now()
  comma = (",")
  end = (";")
  lat_res = lat_sites(SITES)
  # print (now.strftime("%Y-%m-%d %H:%M:%S")),(comma),"Successful Pings",(comma),(success),(end)
  # uncomment above to print to terminal window
  # when success = 0 switch your relays.
  if success <= PINGTHRESH:
    with open(LOGPATH, "a+") as file_object:
      file_object.write("\n")
      file_object.write(now.strftime("%Y-%m-%d %H:%M:%S"))
      file_object.write(comma)
      file_object.write("Successful Pings")
      file_object.write(comma)
      file_object.write(str(success))
      file_object.write(comma)
      file_object.write("Resetting, waiting 5 minutes")
      file_object.write(end)
    GPIO.output(18, True)
    time.sleep(10)
    GPIO.output(18, False)
    time.sleep(300)
  else:
    if lat_res >= LATTHRESH:
      with open(LOGPATH, "a+") as file_object:
        file_object.write("\n")
        file_object.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        file_object.write(comma)
        file_object.write("Latency:")
        file_object.write(str(lat_res))
        file_object.write("ms")
        file_object.write(comma)
        file_object.write("Latency Too High")
        file_object.write(comma)
        file_object.write("Resetting, waiting 5 minutes")
        file_object.write(end)
      GPIO.output(18, True)
      time.sleep(10)
      GPIO.output(18, False)
      time.sleep(300)
    else:
      with open(LOGPATH, "a+") as file_object:
        file_object.write("\n")
        file_object.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        file_object.write(comma)
        file_object.write("Successful Pings")
        file_object.write(comma)
        file_object.write(str(success))
        file_object.write(comma)
        file_object.write("Latency:")
        file_object.write(str(lat_res))
        file_object.write("ms")
        file_object.write(comma)
        file_object.write("Waiting 2 minutes")
        file_object.write(end)
      time.sleep(DELAY_BETWEEN_TESTS)
