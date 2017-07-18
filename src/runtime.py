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

### Tool runtime file

import os
import subprocess
import click

class Runtime:
		def __init__(self):
			pass
## --------------------------------------------------------------------------

		# Get the IDs of containers running
		def getContainerID(self, num):
			try:
				containerIDs = []
				res = subprocess.check_output("docker ps | grep docker_fio", \
												shell=True)
				for cont in res.split("\n"):
						id = cont.split(" ")[0]
						if id:
								containerIDs.append(cont.split(" ")[0])
				return containerIDs
			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)

## -------------------------------------------------------------------------

		# run Fio based on parameters and number of containers
		def runTool(self,tool, containerIDs, fioParams, nvmeParams):
			try:
				print "\n"
				with click.progressbar(containerIDs) as bar:
					for id in bar:

							#if tool is fio tool=1
							if tool == 1:
								print "\nRunning Fio inside container:%s"%id
								cmd = "docker exec "+id+" fio "+fioParams
								res = subprocess.check_output(cmd, shell=True)
								print res+"\n\n\n"
								## --- Print properly ---
								print res.split("\n")[6].split(",")[2]
							
							# if tool is nvme tool=2
							elif tool == 2:
								print "\nRunning NVMe-CLI inside container:%s"%id
								cmd = "docker exec "+id+" nvme "+nvmeParams
								res = subprocess.check_output(cmd, shell=True)
								print res
							else:
								## Run both here parallel
								print "\nRunning Fio and NVMe-CLI inside container:%s"%id
								cmd = "docker exec "+id+" fio "+fioParams+\
									  " & nvme "+nvmeParams
								res = subprocess.check_output(cmd, shell=True)
								print res

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)
