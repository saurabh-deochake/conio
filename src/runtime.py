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
								print "\nSummary for container:%s"%id
								self.summarize(tool, res)
							
							# if tool is nvme tool=2
							elif tool == 2:
								print "\nRunning NVMe-CLI inside container:%s"%id
								cmd = "docker exec "+id+" nvme "+nvmeParams
								res = subprocess.check_output(cmd, shell=True)
								print "\nSummary for container:%s"%id
								self.summarize(tool, res)
							else:
								## Run both here parallel
								print "\nRunning Fio and NVMe-CLI inside container:%s"%id
								cmd = "docker exec "+id+" fio "+fioParams+\
									  " & nvme "+nvmeParams
								res = subprocess.check_output(cmd, shell=True)
								print "\nSummary for container:%s"%id
								self.summarize(tool, res)

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)

## -------------------------------------------------------------------------

		# print the output on screen
		def summarize(self, tool, res):
			try:
				if tool == 1:
					lines = res.split("\n")
					print "\nFIO I/O benchmark:"
					print "> Operation: "+lines[0].split(",")[0].split(":")[2].split("=")[1]
					print "> Jobs: "+lines[3].split(" ")[1]
					print "> Blocksize: "+lines[0].split(",")[1].split("=")[1].split("-")[0]
					print "> Iodepth: "+lines[0].split(",")[3].split("=")[1]
					print "> IOPS: "+lines[6].split(",")[2].split("=")[1]
					print "> Bandwidth: "+lines[6].split(",")[1].split("=")[1]
					print "> Avg. Latency: "+lines[8].split(",")[2].split("=")[1]+" usec"
					print "> 99.99 Latency: "+lines[15].split(" ")[-1][:-1]+" usec"
				if tool == 2:
					lines = res.split("\n")
					print "\nNVMe-CLI:"
					print "> Temperature: "+lines[2].split(":")[1]
					print "> Available Spare: "+lines[3].split(":")[1]
					print "> Percent Used: "+lines[5].split(":")[1]
					print "> Data Units Read: "+lines[6].split(":")[1]
					print "> Data Units Written: "+lines[7].split(":")[1]
				if tool == 3:
					lines = res.split("\n")
					print "\nFIO I/O benchmark:"
					print "> Operation: "+lines[18].split(",")[0].split(":")[2].split("=")[1]
					print "> Jobs: "+lines[21].split(" ")[1]
					print "> Blocksize: "+lines[18].split(",")[1].split("=")[1].split("-")[0]
					print "> Iodepth: "+lines[18].split(",")[3].split("=")[1]
					print "> IOPS: "+lines[24].split(",")[2].split("=")[1]
					print "> Bandwidth: "+lines[24].split(",")[1].split("=")[1]
					print "> Avg. Latency: "+lines[26].split(",")[2].split("=")[1]+" usec"
					print "> 99.99 Latency: "+lines[33].split(" ")[-1][:-1]+" usec"

					# NVME
					print "\nNVMe-CLI:"
					print "> Temperature: "+lines[2].split(":")[1]
					print "> Available Spare: "+lines[3].split(":")[1]
					print "> Percent Used: "+lines[5].split(":")[1]
					print "> Data Units Read: "+lines[6].split(":")[1]
					print "> Data Units Written: "+lines[7].split(":")[1]

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)
