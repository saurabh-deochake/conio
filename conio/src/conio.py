#!/usr/bin/env python

##
# Copyright (c)  2017 Intel Corporation. All rights reserved
# This software and associated documentation (if any) is furnished
# under a license and may only be used or copied in accordance
# with the terms of the license. Except as permitted by such
# license, no part of this software or documentation may be
# reproduced, stored in a retrieval system, or transmitted in any
# form or by any means without the express written consent of
# Intel Corporation.
##


## Handle command line parameters to the tools

import verify as verify
import click 
import os

from config import *
from runtime import Runtime
from container import Container
from ConfigParser import RawConfigParser

## Global flag for disk type
flag = 0

## --------------------------------------------------------------------------
@click.group()
@click.version_option(version='1.0.4')
def conio():
	"""
	Conio- A lightweight tool for containerized I/O benchmarking of NVMe-based cloud storage 
	"""
	if os.getuid() != 0:
		print "[ERROR] Cannot run with non-root user. Aborting!"
		exit(1)
	pass
## -------------------------------------------------------------------------

# List all containers
@conio.command()
@click.option('--running', is_flag=True,
				help="list all running containers")
@click.option('--stopped', is_flag=True,
				help="list all stopped containers")
def list(running, stopped):
	""" 
	list all available containers
	"""
	try:
		c = Container()
		if running:
			running_tag = 1 # list all running containers, 0 otherwise
			data = c.list_containers(running_tag)
		if stopped:
			running_tag = 0
			data = c.list_containers(running_tag)
		else:
			running_tag = 1
			data = c.list_containers(running_tag)
		print "\nCONTAINER ID\tNAMES"
		print "--------------------------------------"
		for key in data:
			print key+"\t"+data[key]
	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)
		exit(1)

## -------------------------------------------------------------------------

# Stop containers for later use
@conio.command()
@click.option('--name', help='name of container to stop')
@click.option('--id', help='ID of container to stop')
@click.option('--all', is_flag=True,
				help='stop all running containers')
def stop(name, id, all):
	"""
	stop containers for later use
	"""
	try:
		if os.getuid() != 0:
			print "[ERROR] Cannot run with non-root user. Aborting!"
			exit(1)
		c = Container()
		if all:
			ids = c.get_container_id(10)
			c.stop_containers(ids)
		if name:
			c.stop_containers(name)
		if id:
			c.stop_containers(id)

	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		exit(1)

## -------------------------------------------------------------------------

# Start stopped containers for benchmarking
@conio.command()
@click.option('--name', help='name of stopped container to start')
@click.option('--id', help='ID of stopped container to start')
@click.option('--all', is_flag=True,
				help='start all stopped containers')

def start(name, id, all):
	"""
	start stopped containers for benchmarking
	"""
	try:
		if os.getuid() != 0:
			 print "[ERROR] Cannot run with non-root user. Aborting!"
			 exit(1)
		c = Container()
		if all:
			running = 0
			c = Container()
			ids = c.list_containers(running).keys()
			c.start_containers(ids)
		if name:
			c.start_containers(name)
		if id:
			c.start_containers(id)
	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)
		exit(1)


## -------------------------------------------------------------------------

# Stop and remove containers
@conio.command()
@click.option('--name', help='name of container to remove')
@click.option('--id', help='ID of container to remove')
@click.option('--num', help='number of containers to remove')
@click.option('--all', is_flag=True,
				help='stop and remove all containers')
#@click.pass_context()
def clean(name, id, num, all):
	"""stop and remove containers"""
 	try:
		if os.getuid() != 0:
			print "[ERROR] Cannot run with non-root user. Aborting!"
			exit(1)
		
		if all:
			c = Container()
			ids = c.get_container_id(10)
			c.cleanup(ids)
		elif num:
			if num == '0':
				print "\n[INFO] Nothing to clean"
				exit(0)
			else:		   
				c = Container()
				ids = c.get_container_id(10)
				ids = ids[:int(num)]
				#print "\n[INFO] Removing first %s container(s)"%num
				c.cleanup(ids)
					
		if name:
			c = Container()
			c.cleanup_specific(name)
		if id:
			c = Container()
			c.cleanup_specific(id)
		else:
				num = raw_input("How many containers do you want to remove:")
				if num == '0':
					print "\n[INFO] Nothing to clean"
					pass
				else:
					c = Container()
					ids = c.get_container_id(10)
					ids = ids[:int(num)]
					#print "\n[INFO] Removing first %s container(s)"%num
					c.cleanup(ids)
		
	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)
		exit(1)

## -------------------------------------------------------------------------

# create --num containers
@conio.command()
@click.option('--num', default=1,
				help='number of containers to spawn for benchmarking')

def create(num):
	"""create and launch containers"""
	try:
		if os.getuid() != 0:
			print "[ERROR] Cannot run with non-root user. Aborting!"
			exit(1)

		global flag
		# check if Docker is set up properly
		d = verify.Verify()
		#res = d.verifyEnvironment()

		c = Container()
		#if not then set up all containers that are required ("num")
		#if not res:
		_, location = c.setup_benchmark_container(num)
		ids = c.get_container_id(num)
		if "nvme" not in location: flag=1
		

	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)
		exit(1)


## -------------------------------------------------------------------------

# all the options
@conio.command()
#@click.pass_context()
@click.option('--tool',default='all',type=click.Choice(['fio','nvme','all']),
				help='I/O benchmark tools to run: fio/nvme/all (both: default)')
@click.option('--num', default=1,
				help='number of containers to benchmark')
@click.option('--thread',default="1",
				help='run jobs as threads')
@click.option('--direct', default="1",
				help='force Direct I/O')
@click.option('--group_reporting', default="1",
				help='get consolidated result for all job threads/processes')
@click.option('--ioengine',default='libaio',type=click.Choice(['libaio','sync']),
				help='I/O engine for the I/O operations for the jobs')
@click.option('--size', default='100%',
				help='total size of I/O operations benchmarking')
@click.option('--do_verify',default="0",
				help='run the verify phase after a write phase')
@click.option('--time_based',default="1",
				help='run time based I/O benchmark tests')
@click.option('--cpus_allowed_policy',default='split',
				help='set CPU affinity for the job')
@click.option('--iodepth',default="32",
				help='set IODepth for this job')
@click.option('--rw',default='randread',type=click.Choice(['randread','randwrite','read','write']),
				help='run sequential/random read and/or operations')
@click.option('--blocksize', default='4k',
				help='set the blocksize for this job')
@click.option('--runtime',default="60",
				help='time (in minutes) this job will run for')
@click.option('--numjobs',default="4",
				help='number of jobs to carry out benchmarking')
#@click.option('--filename',default='/dev/nvme0n1',
#				help='Path to your disk to run benchmark')
@click.option('--name',default='testrun',help='name for your job')
@click.option('--jobfile', help="path to your fio job file")
@click.option('--config', help="path to config file for mixed jobs benchmark")
@click.option('--mixed_jobs', is_flag=True,
				help='set this if you want to run different jobs on containers. (A config file is required)')

@click.option('--offset',
				help='offset in the file to start I/O. Data before the offset will not be touched. Mention size and offset to avoid containers reading over each other')
@click.option('--graph', is_flag=True,
				help='display results in graphical form')
## ------------------------------------------------------------------------

# command function, handles all parameters
def run(tool,num,thread,direct,group_reporting,ioengine,size,do_verify,
				time_based,cpus_allowed_policy,iodepth,rw,blocksize,runtime,
				numjobs,name,jobfile,config,mixed_jobs,offset,graph):
	"""run tools inside containers"""
	try:
		global flag
		if os.getuid() != 0:
			print "\n[ERROR] Cannot run with non-root user. Aborting!"
			exit(1)
		print "\nConio- A lightweight tool for containerized I/O benchmarking of NVMe SSDs"
		print "Copyright Intel Corporation. 2017."
		#location = ""	
		if mixed_jobs:
			if not config:
				print "\n[ERROR] Config file not provided. Aborting!"
				exit(1)
			else:
				if os.path.exists(config) and os.path.isfile(config):
						parser = RawConfigParser()
						parser.read(config)
						num = len(parser.sections())
						#global flag
						# check if Docker is set up properly
						d = verify.Verify()
						res = d.verify_environment()
						c = Container()
						rt = Runtime()

						graph=1 if graph else 0
						# if not then set up all containers that are required ("num")
						if not res:
							_, location = c.setup_benchmark_container(num)
							ids = c.get_container_id(num)
							if "nvme" not in location: flag=1
						elif num>res:
							_, location = c.setup_benchmark_container(num-res)
							ids = c.get_container_id(num)
							if "nvme" not in location: flag=1
						else:
							ids = c.get_container_id(num)
							print "\t-Already have enough containers running, fetching first %s containers"%num
						ids = ids[:num]

						if tool.lower()=="nvme".lower():
							if flag:
								print "\n[ERROR] NVMe-CLI does not work on HDD"
								exit(1)
							else:
								tools = 2
								fioParams = None
								nvmeParams = "smart-log "+CONT_MOUNT
								###-------------- graph plot ------------ ###
								rt.run_tool(tool, ids,fioParams,nvmeParams,graph)
						else:
							tools = 1 if flag else 3
							#tools = 3
							fioParams = []
							nvmeParams = "smart-log "+CONT_MOUNT
							for each_section in parser.sections():
								param = ""
								for (each_key, each_val) in parser.items(each_section):
									param += " --"+each_key+"="+each_val
								fioParams.append(param)

							rt.run_tool(tools, ids, None, None,fioParams, nvmeParams,graph)
	
				else:
					print "\n[Error] No such file or directory!"
					exit(1)
	
		else:	
	
			# check if Docker is set up properly
			d = verify.Verify()
			res = d.verify_environment()
			#global flag
			rt = Runtime()
			c = Container()

			graph=1 if graph else 0
			# if not then set up all containers that are required ("num")
			if not res:
				_,location=c.setup_benchmark_container(num)
				ids = c.get_container_id(num)
				if ("nvme" not in location) and (tool=="nvme" or tool=="all"): flag=1
			elif num>res:
				_,location=c.setup_benchmark_container(num-res)
				ids = c.get_container_id(num)
				if ("nvme" not in location) and (tool=="nvme" or tool=="all") : flag=1
			else:
				ids = c.get_container_id(num)
				print "\t-Already have enough containers running, fetching first %s containers"%num
			ids = ids[:num]
			#print ids
			# which tool do you want to run?
			if tool.lower() == "fio".lower():
				tools = 1
				nvmeParams = None
				if jobfile:
					if os.path.exists(jobfile):
						path = os.path.abspath(jobfile)
						c.copy_to_docker(ids,path)
						fioParams= "/"+os.path.basename(jobfile)
				else:

					fioParams = "--filename="+CONT_MOUNT+" --name="+name+" --thread="+thread + \
					" --direct="+direct+" --group_reporting="+group_reporting+ \
					" --ioengine="+ioengine+" --size="+size+"  --do_verify="+do_verify+ \
					" --time_based="+time_based+" --cpus_allowed_policy="+cpus_allowed_policy+ \
					" --iodepth="+iodepth+" --rw="+rw+" --blocksize="+blocksize+ \
					" --runtime="+runtime+" --numjobs="+numjobs
					# run the tool inside containers
				
				if offset is not None and size is not None:	
					rt.run_tool(tools,ids,offset,size,fioParams,nvmeParams,graph)
				else: 
					rt.run_tool(tools,ids,None,None,fioParams,nvmeParams,graph)

			# nvme-cli
			elif tool.lower() == "nvme".lower():
				if flag:
					print "\n[ERROR] NVMe-CLI does not work on HDD"
					exit(1)
				else:
					tools = 2
					fioParams = None
					nvmeParams = "smart-log "+CONT_MOUNT
					rt.run_tool(tools, ids,None,None,fioParams,nvmeParams,graph)
			# fio and nvme-cli
			else:
				tool = "all"
				tools=1 if flag else 3
				
								
				if jobfile:
					if os.path.exists(jobfile):
						path = os.path.abspath(jobfile)
						c.copy_to_docker(ids, path)
						fioParams = "/"+os.path.basename(jobfile)
				else:
					# gather all parameters, if not mentioned then take default
					fioParams = "--filename="+CONT_MOUNT+ " --name="+name+" --thread="+thread + \
						" --direct="+direct+" --group_reporting="+group_reporting+ \
						" --ioengine="+ioengine+" --size="+size+"  --do_verify="+do_verify+ \
						" --time_based="+time_based+" --cpus_allowed_policy="+cpus_allowed_policy+ \
						" --iodepth="+iodepth+" --rw="+rw+" --blocksize="+blocksize+ \
						" --runtime="+runtime+" --numjobs="+numjobs
				nvmeParams = "smart-log "+CONT_MOUNT
				if offset is not None and size is not None:
					rt.run_tool(tools, ids,offset,size, fioParams, nvmeParams,graph)
				else:
					rt.run_tool(tools,ids,None,None,fioParams,nvmeParams,graph)

	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)




if __name__ == '__main__':
	conio()

