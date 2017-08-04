#!/bin/pythoni


"""
http://www.apache.org/licenses/LICENSE-2.0.txt
Copyright 2017 Intel Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed 
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
CONDITIONS OF ANY KIND, either express or implied. See the License for the 
specific language governing permissions and limitations under the License.
	
Author: Saurabh Deochake, Intel Corporation
"""

## Handle command line parameters to the tools

import verify as verify
import click 
import os

from runtime import Runtime
from ConfigParser import RawConfigParser

## Global flag for disk type
flag = 0

## --------------------------------------------------------------------------
@click.group()
@click.version_option(version='1.0.2')
def conio():
	"""
	Conio- A lightweight tool for containerized I/O benchmarking of NVMe-based cloud storage 
	"""
	if os.getuid() != 0:
		print "[ERROR] Cannot run with non-root user. Aborting!"
		exit(1)
	pass
## -------------------------------------------------------------------------

# Stop and remove containers
@conio.command()
@click.option('--num', help='Number of containers to remove')
@click.option('--all', is_flag=True,
				help='Stop and remove all containers')
#@click.pass_context()
def clean(num, all):
	"""Stop and remove containers"""
 	try:
		if os.getuid() != 0:
			print "[ERROR] Cannot run with non-root user. Aborting!"
			exit(1)
		
		if all:
			d = verify.Verify()
			rt = Runtime()
			ids = rt.getContainerID(10)
			d.cleanup(ids)
		else:
			if num == None:
				number = int(raw_input("How many containers do you want to remove?:"))
				d = verify.Verify()
				rt = Runtime()
				ids = rt.getContainerID(10)
				ids = ids[:number]
				print "\n[INFO] Removing first %s container(s)"%number
				d.cleanup(ids)
					
			elif num == '0':
				print "\n[INFO] Nothing mentioned to clean"
				pass
			else:
				d = verify.Verify()
				rt = Runtime()
				ids = rt.getContainerID(10)
				ids = ids[:int(num)]
				print "\n[INFO] Removing first %s container(s)"%num
				d.cleanup(ids)
		'''
		rt = Runtime()
		print rt.getContainerID(10)[:2]
		'''
	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)
		exit(1)

## -------------------------------------------------------------------------

# create --num containers
@conio.command()
@click.option('--num', default=1,
				help='Number of containers to spawn for benchmarking')

def create(num):
	"""Create and launch containers"""
	try:
		if os.getuid() != 0:
			print "[ERROR] Cannot run with non-root user. Aborting!"
			exit(1)

		global flag
		# check if Docker is set up properly
		d = verify.Verify()
		#res = d.verifyEnvironment()

		rt = Runtime()
		#if not then set up all containers that are required ("num")
		#if not res:
		_, location = d.setupBenchmarkContainer(num)
		ids = rt.getContainerID(num)
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
				help='Number of containers to benchmark')
@click.option('--thread',default="1",
				help='Run jobs as threads')
@click.option('--direct', default="1",
				help='Force Direct I/O')
@click.option('--group_reporting', default="1",
				help='Get consolidated result for all job threads/processes')
@click.option('--ioengine',default='libaio',type=click.Choice(['libaio','sync']),
				help='I/O engine for the I/O operations for the jobs')
@click.option('--size', default='100%',
				help='Total size of I/O operations benchmarking')
@click.option('--do_verify',default="0",
				help='Run the verify phase after a write phase')
@click.option('--time_based',default="1",
				help='Run time based I/O benchmark tests')
@click.option('--cpus_allowed_policy',default='split',
				help='Set CPU affinity for the job')
@click.option('--iodepth',default="32",
				help='Set IODepth for this job')
@click.option('--rw',default='randread',type=click.Choice(['randread','randwrite','read','write']),
				help='Run sequential/random read and/or operations')
@click.option('--blocksize', default='4k',
				help='Set the blocksize for this job')
@click.option('--runtime',default="60",
				help='Time (in minutes) this job will run for')
@click.option('--numjobs',default="4",
				help='Number of jobs to carry out benchmarking')
#@click.option('--filename',default='/dev/nvme0n1',
#				help='Path to your disk to run benchmark')
@click.option('--name',default='testrun',help='Name for your job')
@click.option('--jobfile', help="Path to your fio job file")
@click.option('--config', help="Path to config file for mixed jobs benchmark")
@click.option('--mixed_jobs', is_flag=True,
				help='Set this if you want to run different jobs on containers. (A config file is required)')


## ------------------------------------------------------------------------

# command function, handles all parameters
def run(tool,num,thread,direct,group_reporting,ioengine,size,do_verify,
				time_based,cpus_allowed_policy,iodepth,rw,blocksize,runtime,
				numjobs,name,jobfile,config,mixed_jobs):
	"""Run tools inside containers"""
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
					if num == len(parser.sections()):
						#global flag
						# check if Docker is set up properly
						d = verify.Verify()
						res = d.verifyEnvironment()
					
						rt = Runtime()
						# if not then set up all containers that are required ("num")
						if not res:
							_, location = d.setupBenchmarkContainer(num)
							ids = rt.getContainerID(num)
							if "nvme" not in location: flag=1
						elif num>res:
							_, location = d.setupBenchmarkContainer(num-res)
							ids = rt.getContainerID(num)
							if "nvme" not in location: flag=1
						else:
							ids = rt.getContainerID(num)
							print "\t-Already have enough containers running, fetching first %s containers"%num
						ids = ids[:num]

						if tool.lower()=="nvme".lower():
							if flag:
								print "\n[ERROR] NVMe-CLI does not work on HDD"
								exit(1)
							else:
								tools = 2
								fioParams = None
								nvmeParams = "smart-log /dev/xvda"
								rt.runTool(tool, ids,fioParams,nvmeParams)
						else:
							tools = 1 if flag else 3
							#tools = 3
							fioParams = []
							nvmeParams = "smart-log /dev/xvda"
							for each_section in parser.sections():
								param = ""
								for (each_key, each_val) in parser.items(each_section):
									param += " --"+each_key+"="+each_val
								fioParams.append(param)
							rt.runTool(tools, ids, fioParams, nvmeParams)				
							#print fioParams
					else:
						print "\n[ERROR] Number of containers mentioned does not match that of in config file"
						print "\nAborting!"
						exit(1)
						
						
						
	
				else:
					print "\n[Error] No such file or directory!"
					exit(1)
	
		else:	
	
			# check if Docker is set up properly
			d = verify.Verify()
			res = d.verifyEnvironment()
			#global flag
			rt = Runtime()
			# if not then set up all containers that are required ("num")
			if not res:
				_,location=d.setupBenchmarkContainer(num)
				ids = rt.getContainerID(num)
				if ("nvme" not in location) and (tool=="nvme" or tool=="all"): flag=1
			elif num>res:
				_,location=d.setupBenchmarkContainer(num-res)
				ids = rt.getContainerID(num)
				if ("nvme" not in location) and (tool=="nvme" or tool=="all") : flag=1
			else:
				ids = rt.getContainerID(num)
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
						d.copyToDocker(ids,path)
						fioParams= "/"+os.path.basename(jobfile)
				else:
					fioParams = "--filename=/dev/xvda"+" --name="+name+" --thread="+thread + \
					" --direct="+direct+" --group_reporting="+group_reporting+ \
					" --ioengine="+ioengine+" --size="+size+"  --do_verify="+do_verify+ \
					" --time_based="+time_based+" --cpus_allowed_policy="+cpus_allowed_policy+ \
					" --iodepth="+iodepth+" --rw="+rw+" --blocksize="+blocksize+ \
					" --runtime="+runtime+" --numjobs="+numjobs
					# run the tool inside containers
				rt.runTool(tools,ids, fioParams,nvmeParams)

			# nvme-cli
			elif tool.lower() == "nvme".lower():
				if flag:
					print "\n[ERROR] NVMe-CLI does not work on HDD"
					exit(1)
				else:
					tools = 2
					fioParams = None
					nvmeParams = "smart-log /dev/xvda"
					rt.runTool(tools, ids,fioParams,nvmeParams)
			# fio and nvme-cli
			else:
				tool = "all"
				tools=1 if flag else 3
				
								
				if jobfile:
					if os.path.exists(jobfile):
						path = os.path.abspath(jobfile)
						d.copyToDocker(ids, path)
						fioParams = "/"+os.path.basename(jobfile)
				else:
					# gather all parameters, if not mentioned then take default
					fioParams = "--filename=/dev/xvda "+ "--name="+name+" --thread="+thread + \
						" --direct="+direct+" --group_reporting="+group_reporting+ \
						" --ioengine="+ioengine+" --size="+size+"  --do_verify="+do_verify+ \
						" --time_based="+time_based+" --cpus_allowed_policy="+cpus_allowed_policy+ \
						" --iodepth="+iodepth+" --rw="+rw+" --blocksize="+blocksize+ \
						" --runtime="+runtime+" --numjobs="+numjobs
				nvmeParams = "smart-log /dev/xvda"
				rt.runTool(tools, ids, fioParams, nvmeParams)

		# stop and remove containers
		d.cleanup(ids)
		#clean(ids)
	
	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)




if __name__ == '__main__':
	conio()

