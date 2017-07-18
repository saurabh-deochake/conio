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
				out = []
				for id in containerIDs:
					#if tool is fio tool=1
					if tool == 1:
						print "Running Fio inside container:%s"%id
						cmd = "docker exec "+id+" fio "+fioParams
						res = subprocess.check_output(cmd, shell=True)
						#print "\nSummary for container:%s"%id
					#	print res+"\n\n"
						out.append(self.process(id, tool, res))
					#	self.summarize(out)
							
					# if tool is nvme tool=2
					elif tool == 2:
						print "Running NVMe-CLI inside container:%s"%id
						cmd = "docker exec "+id+" nvme "+nvmeParams
						res = subprocess.check_output(cmd, shell=True)
						#print "\nSummary for container:%s"%id
						out.append(self.process(id, tool, res))
					#	self.summarize(out)
					else:
						## Run both here parallel
						print "Running Fio and NVMe-CLI inside container:%s"%id
						cmd = "docker exec "+id+" fio "+fioParams+\
									  " & nvme "+nvmeParams
						res = subprocess.check_output(cmd, shell=True)
						#print res+"\n\n"
								
						#print "\nSummary for container:%s"%id
						out.append(self.process(id, tool, res))
								
				self.summarize(out)

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)

## -------------------------------------------------------------------------

		# Process the output and store it in dictionary
		def process(self, id, tool, res):
			try:
				output = {}
				output[id] = {}
				if tool == 1:
					lines = res.split("\n")
					op = res.split("Starting")[1].split("\n")
					output[id]['Operation'] = lines[0].split(",")[0].split(":")[2].split("=")[1]
					output[id]['Jobs'] = op[2].split(" ")[2].split("=")[1].split(")")[0]
					output[id]['Blocksize'] = lines[0].split(",")[1].split("=")[1].split("-")[0]
					output[id]['Iodepth'] = lines[0].split(",")[3].split("=")[1]
					output[id]['IOPS'] = op[3].split(",")[2].split("=")[1]
					output[id]['Bandwidth'] = op[3].split(",")[1].split("=")[1]
					output[id]['Avg Latency'] = op[5].split(",")[2].split("=")[1]+" usec"
					output[id]['99.99 Latency'] = op[12].split(" ")[-1][:-1]+" usec"
				if tool == 2:
					lines = res.split("\n")
					output[id]['Temperature'] = lines[2].split(":")[1]
					output[id]['Available Spare'] = lines[3].split(":")[1]
					output[id]['Percent Used'] = lines[5].split(":")[1]
					output[id]['Data Units Read'] = lines[6].split(":")[1]
					output[id]['Data Units Written'] = lines[7].split(":")[1]
				if tool == 3:
					lines = res.split("\n")
					op = res.split("Starting")[1].split("\n")
					output[id]['Operation'] = lines[18].split(",")[0].split(":")[2].split("=")[1]
					output[id]['Jobs'] = op[2].split(" ")[2].split("=")[1].split(")")[0]
					output[id]['Blocksize'] = lines[18].split(",")[1].split("=")[1].split("-")[0]
					output[id]['Iodepth'] = lines[18].split(",")[3].split("=")[1]
					output[id]['IOPS'] = op[3].split(",")[2].split("=")[1]
					output[id]['Bandwidth'] = op[3].split(",")[1].split("=")[1]
					output[id]['Avg Latency'] = op[5].split(",")[2].split("=")[1]+" usec"
					output[id]['99.99 Latency'] = op[12].split(" ")[-1][:-1]+" usec"

					#NVME
					output[id]['Temperature'] = lines[2].split(":")[1]
					output[id]['Available Spare'] = lines[3].split(":")[1]
					output[id]['Percent Used'] = lines[5].split(":")[1]
					output[id]['Data Units Read'] = lines[6].split(":")[1]
					output[id]['Data Units Written'] = lines[7].split(":")[1]
				
				return output
			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)
## -------------------------------------------------------------------------

		# print the output on screen
		def summarize(self, output):
			try:
				for output in output:
					for key  in output:
						print "\n---Summary for container:%s---"%key
						for innerkey in output[key]:
							print innerkey+"="+output[key][innerkey]

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)
