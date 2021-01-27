#!/bin/sh

# Author : @reharish
# ScriptName : Host Finder
# Description : This script will run through your network ip addresses,so that,
#		it will collect IP address of hosts which are UP now.

is_host_up () {
        ping -c 1 $1 > /dev/null
        [ $? -eq 0 ] && echo $1 : Host is up 
}

if [ $# -eq 1 ]
then
MyIpAdd=$(ifconfig $1 | tail -n 8 | head -n 1 | cut -d " " -f 10)
        #echo $MyIpAdd
        MyNetwork=$(ifconfig $1 | tail -n 8 | head -n 1 | cut -d " " -f 10 | cut -d "." -f 1-3)
for i in $MyNetwork.{1..254}
do
   if [ $i != $MyIpAdd ]
   then
   is_host_up $i & disown
   else
       echo "$i : Your IP address"
   fi
done
	exit 0
else
	echo "Invalid Argument"
	echo "USAGE : $0 <NetworkInterface i,e wlan0,eth0,wlp2s0,enp1s0 >"
	exit 111
	echo Terminated With error code $?
fi
