#!/bin/sh

# Author : @reharish
# ScriptName : Host Finder
# Description : This script will run through your network ip addresses,so that,
#		it will collect IP address of hosts which are UP now.

is_host_up () {
        if ping -c 1 $1 &> /dev/null:
	then
        	echo $1 : Host is up 
	fi
}

if [ $# -eq 1 -a ifconfig $1 &>/dev/null ]
then
MyIpAdd=$(ifconfig $1 | grep inet | grep -v pre | cut -d " " -f 10 )
        #echo $MyIpAdd
MyNetwork=$(echo $MyIpAdd | cut -d "." -f 1-3)

for i in $MyNetwork.{1..254}
do
   if [ $i != $MyIpAdd ]
   then
   is_host_up $i & disown
   continue
   else
       echo "$i : Your IP address"
   fi
done


 
else
	echo -e "\e[31m Invalid Argument - Couldn't find the Interface $1\e[0m"
	echo 
	echo -e "\e[32m USAGE : $0 <NetworkInterface i,e wlan0,eth0,wlp2s0,enp1s0 >\e[0m"
	exit 111
	echo Terminated With error code $?
fi

exit 0 
