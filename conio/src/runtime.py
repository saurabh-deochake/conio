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
import re

from ascii_graph import Pyasciigraph
from config import *

class Runtime:
		def __init__(self):
			pass
## --------------------------------------------------------------------------


		# run Fio based on parameters and number of containers
		def runTool(self,tool, containerIDs,offset, size, fioParams, nvmeParams,\
						graph):
			try:
				
				if type(fioParams) is list:
					print "\nNow running Fio and NVMe-CLI inside containers..."
					fio = " bash -c \"fio "
					nvme = " & nvme "+nvmeParams+" > "+NVME_OUT+"\" & "
					cmd = ""

					#print fioParams
					for id, param in zip(containerIDs,fioParams):
						print "\t-Inside container:%s"%id
						cmd += DOCKER_EXEC+" "+id+ fio+" --name=test "+param+" --output="+FIO_OUT+nvme
					
					res = subprocess.check_output(cmd, shell=True)
				
				else:
					print "\nGo grab some coffee while I finish benchmarking your containers!\n"
					#if tool is fio tool=1
					if tool == 1:
						

						fio = " fio "+fioParams+" --output="+FIO_OUT
						cmd = ""
						
						if offset is not None and size is not None and '%' not in size:
							offset = int(offset) 
							
							if offset%512:
								offset -= (offset%512)
								print "[WARNING] Rounding the offset down to nearest 512"
							size = self.convertToBytes(size)
							print "Now running Fio inside containers..."
							for id in containerIDs:
								print "\t-Inside container:%s"%id
								cmd += DOCKER_EXEC+id+fio+" --offset="+str(offset)+" & "
								offset += size 
								
						else:
							print "Now running Fio inside containers..."
							for id in containerIDs:
								print "\t-Inside container:%s"%id
								cmd += DOCKER_EXEC+id+fio+" & "
					
						
						res = subprocess.check_output(cmd, shell=True)
							
					# if tool is nvme tool=2
					elif tool == 2:
						print "Now running NVMe-CLI inside containers..."
						nvme = " bash -c \" nvme "+nvmeParams+" > "+NVME_OUT+"\" & "
						cmd = ""
						for id in containerIDs:
							#print "\t-Inside container:%s"%id
							cmd += DOCKER_EXEC+id+nvme
						res = subprocess.check_output(cmd, shell=True)
						print res
					else:
						## Run both here parallel
						fio = " bash -c \"fio "+fioParams+" --output="+FIO_OUT
						nvme = " nvme "+nvmeParams+" > "+NVME_OUT+"\" &"
						cmd = ""
						
						if offset is not None and size is not None and '%' not in size:
							offset = int(offset)
							if offset%512: 
								offset -= offset%512
								print "[WARNING] Rounding the offset down to nearest 512"
							size = self.convertToBytes(size)
							
							print "Now running Fio and NVMe-CLI inside containers..."
							for id in containerIDs:
								print "\t-Inside container:%s"%id
								cmd += DOCKER_EXEC+id+fio+" --offset="+str(offset)+" & "+nvme
								offset += size
						else:

							print "Now running Fio and NVMe-CLI inside containers..."
							for id in containerIDs:
								print "\t-Inside container:%s"%id
								cmd += DOCKER_EXEC+id+fio+" & "+nvme
						#print cmd
						res = subprocess.check_output(cmd, shell=True)
				
				if graph:
					self.summarizeGraph(tool, containerIDs)
				else:
					self.summarize(tool, containerIDs)

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print "Please note that NVMe-CLI does not work on HDDs"
					print str(e)

## ------------------------------------------------------------------------

	# print the summary of operation
		def summarize(self, tool, containerIDs):
			try:
				if tool == 1:
					for id in containerIDs:
						print "\nSummary for container:%s"%id
						cmd = DOCKER_EXEC+id+" cat "+FIO_OUT
						res = subprocess.check_output(cmd, shell=True)
						lines = res.split("\n")
						op = res.split("Starting")[1].split("\n")
						print "Operation:"+ lines[0].split(",")[0].split(":")[2].split("=")[1]
						print "Jobs:"+ op[2].split(" ")[2].split("=")[1].split(")")[0]
						print "Blocksize:"+ lines[0].split(",")[1].split("=")[1].split("-")[0]
						print "Iodepth:"+ lines[0].split(",")[3].split("=")[1]
						print "IOPS:"+ op[3].split(",")[2].split("=")[1]
						print "Bandwidth:"+ op[3].split(",")[1].split("=")[1]
						print "Avg Latency:"+ op[5].split(",")[2].split("=")[1]+" usec"
						print "99.99 Latency:"+ op[12].split("=")[-1].split("[")[1][:-1]+" usec"

						#print res
				if tool == 2:
					for id in containerIDs:
						print "\nSummary for container:%s"%id
						cmd = DOCKER_EXEC+id+" cat "+NVME_OUT
						res = subprocess.check_output(cmd, shell=True)
						lines = res.split("\n")
						print "Temperature:"+ lines[2].split(":")[1]
						print "Available Spare:" + lines[3].split(":")[1]
						print "Percent Used:" + lines[5].split(":")[1]
						print "Data Units Read:"+ lines[6].split(":")[1]
						print "Data Units Written:"+ lines[7].split(":")[1]
				if tool == 3:
					for id in containerIDs:
						try:
							print "\nSummary for container:%s"%id
							cmd = DOCKER_EXEC+id+" cat "+FIO_OUT
							res = subprocess.check_output(cmd, shell=True)
							print "\n---------FIO------------"
							lines = res.split("\n")
							op = res.split("Starting")[1].split("\n")
							print "Operation:"+ lines[0].split(",")[0].split(":")[2].split("=")[1]
							print "Jobs:"+ op[2].split(" ")[2].split("=")[1].split(")")[0]
							print "Blocksize:"+ lines[0].split(",")[1].split("=")[1].split("-")[0]
							print "Iodepth:"+ lines[0].split(",")[3].split("=")[1]
							print "IOPS:"+ op[3].split(",")[2].split("=")[1]
							print "Bandwidth:"+ op[3].split(",")[1].split("=")[1]
							print "Avg Latency:"+ op[5].split(",")[2].split("=")[1]+" usec"
							print "99.99 Latency:"+ op[12].split("=")[-1].split("[")[1][:-1]+" usec"

							cmd = "docker exec "+id+" cat "+NVME_OUT
							res = subprocess.check_output(cmd, shell=True)
							print "\n--------NVME------------"
							lines = res.split("\n")
							print "Temperature:"+ lines[2].split(":")[1]
							print "Available Spare:" + lines[3].split(":")[1]
							print "Percent Used:" + lines[5].split(":")[1]
							print "Data Units Read:"+ lines[6].split(":")[1]
							print "Data Units Written:"+ lines[7].split(":")[1]
						except Exception:
							print "\n[ERROR] NVMe-cli does not work on HDD"
							pass

			except Exception, e:
				print "\n[ERROR] Something went wrong. Try again!"
				print "\nNVMe-CLI only works on NVMe Solid State Drives"
				exit(1)

## -------------------------------------------------------------------------

		# Summarize in graphical form
		def summarizeGraph(self, tool, containerIDs):
			try:
				
				iops = []
				bandwidth = []
				avglat = []
				_99lat = []
				dread = []
				dwrite = []
				graph = Pyasciigraph(line_length=80,min_graph_length=30,float_format='{0:,.2f}')
				non_decimal = re.compile(r'[^\d.]+')
				print "\n\t\t     ---Summary of benchmark results---"
				if tool == 1:
					for id in containerIDs:
						#print "\nSummary for container:%s"%id
						cmd = DOCKER_EXEC+id+" cat "+FIO_OUT
						res = subprocess.check_output(cmd, shell=True)
						lines = res.split("\n")
						op = res.split("Starting")[1].split("\n")

						info = lines[0].split(",")[0].split(":")[2].split("=")[1]+\
								" bs="+\
								lines[0].split(",")[1].split("=")[1].split("-")[0]+\
								" Qd="+lines[0].split(",")[3].split("=")[1]+\
								" jobs="+op[2].split(" ")[2].split("=")[1].split(")")[0]+\
								" id="+id
						iops_data = (info,int(op[3].split(",")[2].split("=")[1]))
						 
						bandwidth_data = (info, float(non_decimal.sub('',op[3].split(",")[1].split("=")[1]))/1000)
						avglat_data = (info, float(op[5].split(",")[2].split("=")[1]))
						_99lat_data = (info, float(op[12].split("=")[-1].split("[")[1][:-1]))
						iops.append(iops_data)
						bandwidth.append(bandwidth_data)
						avglat.append(avglat_data)
						_99lat.append(_99lat_data)

				
					print "\n\t\t\t\t--FIO--"
					for line in graph.graph('IOPS',iops):
						print line
					print"\n"	
					for line in graph.graph("Bandwidth (MB/s)",bandwidth):
						print line
					print "\n"
					for line in graph.graph('Average Latency (usec)',avglat):
						print line
					print "\n"
					for line in graph.graph('99.99% Latency (usec)',_99lat):
						print line
				
				if tool == 2:
					for id in containerIDs:
						cmd = DOCKER_EXEC+id+" cat "+NVME_OUT
						res = subprocess.check_output(cmd, shell=True)
						lines = res.split("\n")
				
						info = "Temp="+lines[2].split(":")[1]+\
							   " Avail Spare="+lines[3].split(":")[1]+\
							   " Used:"+lines[5].split(":")[1]+\
							   " id:"+id
						dread_data = (info,int(lines[6].split(":")[1]))
						dwrite_data = (info,int(lines[7].split(":")[1]))

						dread.append(dread_data)
						dwrite.append(dwrite_data)

					print "\n\t\t\t\t--NVMe-Cli--"
					for line in graph.graph('Data Units Read',dread):
						print line
					print "\n"
					for line in graph.graph('Data Units Written',dwrite):
						print line

			

				if tool == 3:
					for id in containerIDs:
						#print "\nSummary for container:%s"%id
						cmd = DOCKER_EXEC+id+" cat "+FIO_OUT
						res = subprocess.check_output(cmd, shell=True)
						lines = res.split("\n")
						op = res.split("Starting")[1].split("\n")
						
						info = lines[0].split(",")[0].split(":")[2].split("=")[1]+\
						      	" bs="+\
						      	lines[0].split(",")[1].split("=")[1].split("-")[0]+\
								" Qd="+lines[0].split(",")[3].split("=")[1]+\
								" jobs="+op[2].split(" ")[2].split("=")[1].split(")")[0]+\
								" id="+id
						iops_data = (info,int(op[3].split(",")[2].split("=")[1]))
						bandwidth_data = (info, float(non_decimal.sub('',op[3].split(",")[1].split("=")[1]))/1000)
						avglat_data = (info, float(op[5].split(",")[2].split("=")[1]))
						_99lat_data = (info, float(op[12].split("=")[-1].split("[")[1][:-1]))
						iops.append(iops_data)
						bandwidth.append(bandwidth_data)
						avglat.append(avglat_data)
						_99lat.append(_99lat_data)
						
						cmd = DOCKER_EXEC+id+" cat "+NVME_OUT
						res = subprocess.check_output(cmd, shell=True)
						lines = res.split("\n")
						
						info = "Temp="+lines[2].split(":")[1]+\
								" Avail Spare="+lines[3].split(":")[1]+\
								" Used:"+lines[5].split(":")[1]+\
								" id:"+id
						dread_data = (info,int(lines[6].split(":")[1]))
						dwrite_data = (info,int(lines[7].split(":")[1]))
						dread.append(dread_data)
						dwrite.append(dwrite_data)

				
					# Now print the graph
					print "\n\t\t\t\t--FIO--"
					for line in graph.graph('IOPS',iops):
						print line
					print"\n"
					for line in graph.graph("Bandwidth (MB/s)",bandwidth):
						print line
					print "\n"
					for line in graph.graph('Average Latency (usec)',avglat):
						print line
					print "\n"
					for line in graph.graph('99.99% Latency (usec)',_99lat):
						print line
					print "\n\t\t\t\t--NVMe-Cli--"
					for line in graph.graph('Data Units Read',dread):
						print line
					print "\n"
					for line in graph.graph('Data Units Written',dwrite):
						print line

						
				inp = raw_input("\nPress \"Y\" to read more or any key to quit:")
				if inp.lower() == "y".lower():
					self.summarize(tool, containerIDs)
				else:
					return
			except Exception, e:
				print "\n[ERROR] Something went wrong. Try again!"
				print str(e)
				exit(1)


## -------------------------------------------------------------------------
		
		# If offset is mentioned, convert KB/MB/GB to B
		def convertToBytes(self, size):
			try:
				size = size.lower()
				# KB or KiB or kb
				if size.find("k".lower()) != -1:
					index = size.find("k".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber << 10
				# sizeInNumber * math.pow(10,3)
				# MB or MiB or mb
				if size.find("m".lower()) != -1:
					index = size.find("m".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber * math.pow(10,6)
				# GB or GiB or gb
				if size.find("g".lower()) != -1:
					index = size.find("g".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber << 30 
					#sizeInNumber * math.pow(10, 9)
				# TB or TiB or tb
			   	if size.find("t".lower()) != -1:
					index = size.find("t".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber << 40 
					#* math.pow(10, 12)
			  	# B or b
			  	if size.find("b".lower()) != -1:
					index = size.find("b".lower())
					return int(size[:index])
			except Exception, e:
				print "\n[ERROR] Failed to get size in bytes"
				print str(e)
				exit(1)

