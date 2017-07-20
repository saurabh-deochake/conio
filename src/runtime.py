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
				# check if docker container with specific image is running
				res = subprocess.check_output("docker ps | grep docker_fio", \
												shell=True)
				#gather ids for all containers
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
				print "\nGo grab some coffee while I finish benchmarking your containers!\n"
				#if tool is fio tool=1
				if tool == 1:
					print "Now running Fio inside containers..."
					fio = " fio "+fioParams+" --output=fio.out &"
					cmd = ""
					for id in containerIDs:
						print "\t-Inside container:%s"%id
						cmd += "docker exec "+id+fio
					
					print cmd
					res = subprocess.check_output(cmd, shell=True)
					for item in res.split("\n"):
							if "iops" in item or "clat" in item:
									print item.strip()
					#out.append(self.process(id, tool, res))
							
				# if tool is nvme tool=2
				elif tool == 2:
					print "Now running NVMe-CLI inside containers..."
					nvme = " bash -c \" nvme "+nvmeParams+" > /nvme.out\" & "
					cmd = ""
					for id in containerIDs:
						print "\t-Inside container:%s"%id
						cmd += "docker exec "+id+nvme
					res = subprocess.check_output(cmd, shell=True)
					print res
					#out.append(self.process(id, tool, res))
				else:
					## Run both here parallel
					print "Now running Fio and NVMe-CLI inside containers..."
					fio = " bash -c \"fio "+fioParams+" --output=fio.out &"
					nvme = " nvme "+nvmeParams+" > /nvme.out\" &"
					cmd = ""
					for id in containerIDs:
						print "\t-Inside container:%s"%id
						cmd += "docker exec "+id+fio+nvme
					print cmd
					res = subprocess.check_output(cmd, shell=True)
					print res
					#out.append(self.process(containerIDs, tool, res))
								
				self.summarize(tool, containerIDs)

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print "Please note that NVMe-CLI does not work on HDDs"
					print str(e)
## -------------------------------------------------------------------------

		# Process the output and store it in dictionary
		def process(self, id, tool, res):
			try:
				# store output for each container
				# use list of dict of dict
				output = {}
				output[id] = {}
				if tool == 1:
					#only fio
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
					#only nvme
					lines = res.split("\n")
					output[id]['Temperature'] = lines[2].split(":")[1]
					output[id]['Available Spare'] = lines[3].split(":")[1]
					output[id]['Percent Used'] = lines[5].split(":")[1]
					output[id]['Data Units Read'] = lines[6].split(":")[1]
					output[id]['Data Units Written'] = lines[7].split(":")[1]
				if tool == 3:
					#both fio and nvme
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

					#NVME part
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
		def summarizeIt(self, output):
			try:
				# print the output for each container 
				for output in output:
					for key  in output:
						print "\n---Summary for container:%s---"%key
						for innerkey in output[key]:
							print innerkey+"="+output[key][innerkey]

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print str(e)

## ------------------------------------------------------------------------

	# print the summary of operation
		def summarize(self, tool, containerIDs):
			try:
				if tool == 1:
					for id in containerIDs:
						print "\nSummary for container:%s"%id
						cmd = "docker exec "+id+" cat /fio.out"
						res = subprocess.check_output(cmd, shell=True)
						print res
				if tool == 2:
					for id in containerIDs:
						print "\nSummary for container:%s"%id
						cmd = "docker exec "+id+" cat /nvme.out"
						res = subprocess.check_output(cmd, shell=True)
						print res
				else:
					for id in containerIDs:
						print "\nSummary for container:%s"%id
						cmd = "docker exec "+id+" cat /fio.out"
						res = subprocess.check_output(cmd, shell=True)
						print "\n---------FIO------------"
						print res
						cmd = "docker exec "+id+" cat /nvme.out"
						res = subprocess.check_output(cmd, shell=True)
						print "\n--------NVME------------"
						print res
			except Exception, e:
				print "\n[ERROR] Something went wrong. Try again!"
				print str(e)

