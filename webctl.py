#!/usr/bin/env python
# coding=utf-8

__author__ = "Eduardo Medeiros <eduardo.medeiros@hp.com>"

import argparse
import ConfigParser
import subprocess
import time
import urllib

config = ConfigParser.ConfigParser()
config.read("webctl.ini")

parser = argparse.ArgumentParser(description="Processando comandos...",usage="%(prog)s [options] [instance]")
parser.add_argument("--start",help="Start an application",nargs="*")
parser.add_argument("--stop",help="Stop an application",nargs="*")
parser.add_argument("--status",help="Status of an application",nargs="*")
parser.add_argument("--info",help="Information of an application",nargs="*")

def url_status(url):
	try:
		return urllib.urlopen(url).getcode()
	except IOError: 
		return None	

def start(inst):
	for i in inst:
		print "Starting %s..." % i
		try:
			start_cmd = config.get(i,"start")
			home_dir = config.get(i,"home_dir")
			
			subprocess.call("cd %s && nohup ./%s" % (home_dir,start_cmd),shell=True)
		
			n = 1
			while True:
				if config.get(i,"check_url_delay"):
					print "Waiting Application startup.."
					time.sleep(config.getfloat(i,"check_url_delay"))
				
				status_code = url_status(config.get(i,"url"))
			
				if status_code in range(200,400):
					print "%s is working properly on url %s" % (i,config.get(i,"url")) 
					break
				else:
					n += 1
				# counter check (5)
				if n == 6:
					print "%s is not working properly" % i
					break

		except ConfigParser.NoSectionError:
			print "Application %s does not exists!" % i
		print "-" * 50

def stop(inst):
	for i in inst:
		print "Stoping %s..." % i
		try:
			stop_cmd = config.get(i,"stop")
			home_dir = config.get(i,"home_dir")

			subprocess.call("cd %s && nohup ./%s" % (home_dir,stop_cmd),shell=True)

		except ConfigParser.NoSectionError:
			print "Application %s does not exists!" % i
		print "-" * 50


def status(inst):
	for i in inst:
		print "Status %s..." % i
		try:
			status_code = url_status(config.get(i,"url"))

			if status_code in range(200,400):
				print "%s is working properly on url %s" % (i,config.get(i,"url")) 
			else:
				print "%s is not working properly" % i
				
		except ConfigParser.NoSectionError:
			print "Application %s does not exists!" % i
		print "-" * 50

if __name__ == "__main__":
	args = parser.parse_args()
	if args.start:
		start(args.start)
	elif args.stop:
		stop(args.stop)
	elif args.status:
		status(args.status)
	elif args.info:
		print u"Informação %s" % args.info[0]
