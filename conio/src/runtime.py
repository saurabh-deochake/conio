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


### Tool runtime file

import os
import subprocess
import click
import re

from ascii_graph import Pyasciigraph
from config import *

class Runtime:
		"""
		Run tools and display results 
		"""
		def __init__(self):
			"""
			Empty constructor. Can be used to initialize variables
			"""
			pass
## --------------------------------------------------------------------------


		# run Fio based on parameters and number of containers
		def run_tool(self, tool, containerIDs, offset, size, fioParams, nvmeParams,\
						graph):
			"""
			Run tools inside the containers according to all the parameters

			:param tool: string, name of tool to run 
			:param containerIDs: list of containers to run tools in
			:param offset: string, offset to start IO from
			:param size: string, size of disk to test
			:param fioParams: string/list of FIO parameters
			:param nvmeParams: string, nvme-cli parameters
			:returns: exit gracefully when done
			:raises Exception: if command fails to execute
			"""
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
							#offset = int(offset) 
							offset = self.convert_to_bytes(offset)
							if offset%512:
								offset -= (offset%512)
								print "[WARNING] Rounding the offset down to nearest 512"
							size = self.convert_to_bytes(size)
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
							size = self.convert_to_bytes(size)
							
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
					self.summarize_graph(tool, containerIDs)
				else:
					self.summarize(tool, containerIDs)

			except Exception, e:
					print "\n[ERROR] Something went wrong. Try again!"
					print "Please note that NVMe-CLI does not work on HDDs"
					print str(e)

## ------------------------------------------------------------------------

	# print the summary of operation
		def summarize(self, tool, containerIDs):
			"""
			Summarize the result in textual form

			:param tool: string, tool which was run in contaier
			:param containerIDs: list of containers id
			:returns: exit gracefully when done
			:raises Exception: if command fails to execute
			"""
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
		def summarize_graph(self, tool, containerIDs):
			"""
			Summarize the result in graphical form
			
			:param tool: string, tool which was run in container
			:param containerIDs: list of containers ids
			:return: exit gracefully when done
			:raises Exception: if command fails to execute
			"""
			try:
				
				iops = []
				bandwidth = []
				avglat = []
				_99lat = []
				dread = []
				dwrite = []
				graph = Pyasciigraph(line_length=80, min_graph_length=30, float_format='{0:,.2f}')
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
					for line in graph.graph('IOPS', iops):
						print line
					print"\n"	
					for line in graph.graph("Bandwidth (MB/s)", bandwidth):
						print line
					print "\n"
					for line in graph.graph('Average Latency (usec)', avglat):
						print line
					print "\n"
					for line in graph.graph('99.99% Latency (usec)', _99lat):
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
					for line in graph.graph('Data Units Read', dread):
						print line
					print "\n"
					for line in graph.graph('Data Units Written', dwrite):
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
						dread_data = (info, int(lines[6].split(":")[1]))
						dwrite_data = (info, int(lines[7].split(":")[1]))
						dread.append(dread_data)
						dwrite.append(dwrite_data)

				
					# Now print the graph
					print "\n\t\t\t\t--FIO--"
					for line in graph.graph('IOPS', iops):
						print line
					print"\n"
					for line in graph.graph("Bandwidth (MB/s)", bandwidth):
						print line
					print "\n"
					for line in graph.graph('Average Latency (usec)', avglat):
						print line
					print "\n"
					for line in graph.graph('99.99% Latency (usec)', _99lat):
						print line
					print "\n\t\t\t\t--NVMe-Cli--"
					for line in graph.graph('Data Units Read', dread):
						print line
					print "\n"
					for line in graph.graph('Data Units Written', dwrite):
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
		def convert_to_bytes(self, size):
			"""
			convert size to number of bytes
			
			:param size: string, size to convert
			:return size: integer in bytes
			:raise Exception: if command fails to execute
			"""
			try:
				size = size.lower()
				# KB or KiB or kb
				if size.find("k".lower()) != -1:
					index = size.find("k".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber << 10
				# sizeInNumber * math.pow(10,3)
				# MB or MiB or mb
				elif size.find("m".lower()) != -1:
					index = size.find("m".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber << 20
				# GB or GiB or gb
				elif size.find("g".lower()) != -1:
					index = size.find("g".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber << 30 
					#sizeInNumber * math.pow(10, 9)
				# TB or TiB or tb
			   	elif size.find("t".lower()) != -1:
					index = size.find("t".lower())
					sizeInNumber = int(size[:index])
					return sizeInNumber << 40 
					#* math.pow(10, 12)
			  	# B or b
			  	elif size.find("b".lower()) != -1:
					index = size.find("b".lower())
					return int(size[:index])
				else: 
					return int(size)
					
			except Exception, e:
				print "\n[ERROR] Failed to get size in bytes"
				print str(e)
				exit(1)

