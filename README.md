# rpi-router-reboot
A python script to check internet connectivity and reboot router upon failure.  This runs on a raspberry pi. 
Base script was found here: https://www.raspberrypi.org/forums/viewtopic.php?t=187918 

# Summary
Living in a rural area, all ISP options routinely "hang" and require a router reboot to restore internet access. This happens at all hours, and generally the equipment will recover fairly quickly provided it is manually reset.  Otherwise, connectivity will be down until the device is power cycled. This script checks connectivity to a google DNS server every 2 minutes, via ICMP ping.  If ping fails, it powercycles the power strip the modem is plugged into, and waits for 5 minutes. Acitivity is logged (helpful for dealing with ISP tech support).

# Hardware 
1 Raspberry Pi (model 3 used, but this shouldn't matter).

1 Power strip with GPIO (https://www.adafruit.com/product/2935 used, anything with a GPIO relay should work) 

1 Ethernet Cable (Not needed if using wifi, NOTE: if auto-reconnect is buggy with the router, the author would definitly reccomend ethernet)

2 Breadboard Jumper wires, (Female/Male)

1 ISP Modem/Router (tested on AT&T DSL/Uverse and Verzion home LTE)

# Diagram
![alt text](https://github.com/commdogg/rpi-router-reboot/blob/main/googs-diag.jpeg?raw=true)

# Additional Config
Place script in 'pi' user home directory.  
To Start script at boot:

Edit '/etc/rc.local'
Add line to end of file 
```bash
sudo python3 /home/pi/google-ping.py &
```
# Auditing
Script will log activity to '/home/pi/googs-log.txt' Use general linux shell commands to read log, eg. for searching the log for ping faulires/resets type:
```bash
cat google-ping-log.txt | grep Resetting
```
This filters for "Resetting" lines and provides time stamps of each reboot. 
