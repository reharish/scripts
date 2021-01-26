#!/bin/sh

# Author : @reharish
# ScriptName : Host Finder
# Description : This script will run through your network ip addresses,so that,
#		it will collect IP address of hosts which are UP now.


#echo $MyIpAdd

is_host_up () {
	ping -c 1 $1 > /dev/null
	[ $? -eq 0 ] && echo $1 : Host is up 
}

if [ $# == 1 ]
then
	MyIpAdd=$(ifconfig $1 | tail -n 8 | head -n 1 | cut -d " " -f 10)
	#echo $MyIpAdd
	MyNetwork=$(ifconfig $1 | tail -n 8 | head -n 1 | cut -d " " -f 10 | cut -d "." -f 1-3)
	if [ "$MyIpAdd" != "" ]
	then
		for i in $MyNetwork.{1..254}
		do
		if [ $i != $MyIpAdd ]
		then
		is_host_up $i & disown
		else
		echo "$i : Your IP address"
		fi
		done
	else
		echo "unable to get IP Address"
		echo "check Your Network Interface"
		echo " "
	fi
else
	echo "Invalid Arguments"
	echo "USAGE : $0 <NetworkInterface i,e wlan0,eth0,wlp2s0,enp1s0 >" 
fi
