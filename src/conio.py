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

# all the options
@click.command()
@click.option('--tool',default='all',type=click.Choice(['fio','nvme','all']),
				help='I/O benchmark tools to run: fio/nvme/all (both: default)')
@click.option('--num', default=1,
				help='Number of containers to spawn for benchmarking')
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
def conio(tool,num,thread,direct,group_reporting,ioengine,size,do_verify,
				time_based,cpus_allowed_policy,iodepth,rw,blocksize,runtime,
				numjobs,name,jobfile,config,mixed_jobs):
	try:
		print "\nConio- A lightweight tool for containerized I/O benchmarking of NVMe SSDs"
		print "Intel Corporation. 2017."
	
		if mixed_jobs:
			if not config:
				print "\n[ERROR] Config file not provided. Aborting!"
				exit(1)
			else:
				if os.path.exists(config) and os.path.isfile(config):
					parser = RawConfigParser()
					parser.read(config)
					if num == len(parser.sections()):
						
						# check if Docker is set up properly
						d = verify.Verify()
						res = d.verifyEnvironment()
					
						rt = Runtime()
						# if not then set up all containers that are required ("num")
						if not res:
							d.setupBenchmarkContainer(num)
							ids = rt.getContainerID(num)
						elif num>res:
							d.setupBenchmarkContainer(num-res)
							ids = rt.getContainerID(num)
						else:
							ids = rt.getContainerID(num)
							print "\t-Already have enough containers running, fetching first %s containers"%num
						ids = ids[:num]

						if tool.lower()=="nvme".lower():
							tool = 2
							fioParams = None
							nvmeParams = "smart-log /dev/xvda"
							rt.runTool(tool, ids,fioParams,nvmeParams)
						else:
							tool = 3
							fioParams = []
							for each_section in parser.sections():
								param = ""
								for (each_key, each_val) in parser.items(each_section):
									param += " --"+each_key+"="+each_val
								fioParams.append(param)
								
							print fioParams
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

			rt = Runtime()
			# if not then set up all containers that are required ("num")
			if not res:
				d.setupBenchmarkContainer(num)
				ids = rt.getContainerID(num)
			elif num>res:
				d.setupBenchmarkContainer(num-res)
				ids = rt.getContainerID(num)
			else:
				ids = rt.getContainerID(num)
				print "\t-Already have enough containers running, fetching first %s containers"%num
			ids = ids[:num]
	
			# which tool do you want to run?
			if tool.lower() == "fio".lower():
				tool = 1
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
				rt.runTool(tool,ids, fioParams,nvmeParams)

			# nvme-cli
			elif tool.lower() == "nvme".lower():
				tool = 2
				fioParams = None
				nvmeParams = "smart-log /dev/xvda"
				rt.runTool(tool, ids,fioParams,nvmeParams)
			# fio and nvme-cli
			else:
				tool = "all"
				tool = 3
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
				rt.runTool(tool, ids, fioParams, nvmeParams)

			# stop and remove containers
			d.cleanup(ids)
	
	except Exception, e:
		print "\n[ERROR] Something went wrong. Try again!"
		print str(e)
if __name__ == '__main__':
	conio()
