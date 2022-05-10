#!/bin/sh

# Author : @reharish
# ScriptName : Host Finder
# Description : This script will run through your network ip addresses,so that,
#		it will collect IP address of hosts which are UP now.

is_host_up ()
{

    if ping -c 1 $1 &> /dev/null;
    then
        printf "$1\n"; 
    fi
}

#echo $1

if ip address show $1 &>/dev/null;
then
    
    MyIPAddress=$(ip a show $1 | grep inet | grep -v inet6 | cut -d "/" -f 1 | tr -d " [a-zA-Z]")

    MyNetwork=$( echo $MyIPAddress | cut -d "." -f 1-3 )

    
    for i in $MyNetwork.{1..254}
    do
	if [ $i != $MyIPAddress ]
	then
	    is_host_up $i & disown
	else
	    printf "$i" # Optional.
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
