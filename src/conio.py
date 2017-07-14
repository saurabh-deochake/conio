#!/bin/python


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

import verify as verify
import click 


@click.command()
@click.option('--tools',default='all',
				help='I/O benchmark tools to run: fio/nvme_cli/all (both, default)')
@click.option('--num', default=1,
				help='Number of containers to spawn for benchmarking')
def conio(tools,num):
	"""Conio- A lightweight script for containerized I/O benchmarking of NVMe SSDs
	"""
	print "\nConio- A lightweight script for containerized I/O benchmarking of NVMe SSDs"
	print "Intel Corporation. 2017."
	
	d = verify.Dockerbench()
	res = d.verifyEnvironment()
	if not res:
		d.setupBenchmarkContainer(num)
	elif num>res:
		d.setupBenchmarkContainer(num-res)
	else:
		print d.getContainerID(num)

	if tools.lower() == "fio".lower():
		print 'We will run %s'%fio
	elif tools.lower() == "nvme_cli".lower():
		print "WE will run %s"%nvme_cli
	else:
		tools = "all"
		print "we will run both ",tools

if __name__ == '__main__':
	conio()
