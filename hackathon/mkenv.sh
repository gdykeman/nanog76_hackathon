#!/bin/sh
if [ ! -d bin ]
then
	echo "Creating python venv."
	python3 -m venv .
fi
. bin/activate
pip install exabgp wheel
pip install networkx scapy
[ -d etc/exabgp ] || mkdir -p etc/exabgp
[ -d run ] || mkdir run
[ -p run/exabgp.in ] || mkfifo run/exabgp.in
[ -p run/exabgp.out ] || mkfifo run/exabgp.out
[ -f etc/exabgp/exabgp.env ] || exabgp --fi > etc/exabgp/exabgp.env

if [ ! -f exabgp.cfg ]
then
	LocalIP=`ip addr list dev eth1 | fgrep 20.0.0. | awk '{print$2}' | cut -d/ -f1`
	Net=`echo ${LocalIP} | cut -d. -f1-3`
	Last=`echo ${LocalIP} | cut -d. -f4`
	RLast=`expr ${Last} - 1`
	RemoteIP="${Net}.${RLast}"
	echo "Creating exabgp.cfg with local=${LocalIP} remote=${RemoteIP}"
	sed -e "s/@LOCAL_IP/${LocalIP}/" <exabgp.in |
	sed -e "s/@REMOTE_IP/${RemoteIP}/" >exabgp.cfg
fi