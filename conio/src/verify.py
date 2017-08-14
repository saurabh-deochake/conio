

#!/bin/python


"""
http://www.apache.org/licenses/LICENSE-2.0.txt
Copyright 2017 Intel Corporation
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Saurabh Deochake, Intel Corporation
"""

import os
import stat
import subprocess
import sys; sys.dont_write_bytecode = True

from config import *

class Verify:
	def __init__(self):
		# check environment variable
		pass

## -------------------------------------------------------------------------
	
	# Verify environment needed to run the tool
	def verifyEnvironment(self):
		if self.verifyDocker():
				if self.verifyDockerdRunning():
						res = self.verifyFioContainer() 
						if not int(res):
							print "\t-[OK] Docker is installed and running"
							return 0
							#self.setupBenchmarkContainer(num)
						else:
							print "\t-[INFO] Docker container for benchmarking already set up"
							return int(res)
							#exit(1)

## --------------------------------------------------------------------------

	# Verify if docker is installed
	def verifyDocker(self):
		try:
			print "\nVerifying Docker enviroment..."
			res = subprocess.check_output(RPM_GREP+" docker", shell=True)
			if res == "":
					print "\t-[ERROR] Is Docker installed? Please install Docker..."
					return False
			else:
					return True
		except Exception, e:
			print "\t-[ERROR] Is Docker installed? Please install Docker..."
			exit(1)

## -------------------------------------------------------------------------
	# Verify if Docker daemon is running
	def verifyDockerdRunning(self):
		try:
			#print "\t...Verifying Docker daemon"
			res = subprocess.check_output(PS_GREP+" dockerd", shell=True)
			if "/usr/bin/dockerd" in res:
					return True
			else:
					print "\t-[ERROR] Docker daemon is not running"
					exit(1)
		except Exception, e:
			print "\n[ERROR] Something went wrong. Please try again..."
			exit(1)

## -------------------------------------------------------------------------

	# Verify if benchmark container is running
	def verifyFioContainer(self):
		try:
			#print "\t...Verifying if benchmark container is set up"
			res = subprocess.check_output(DOCKER_PS_GREP+DOCKER_IMAGE_NAME+"| wc -l",\
							shell=True)
			# return the output 	
			return res
		except Exception, e:
				 print "\t-[ERROR] Benchmark container is not running"
				 inp = raw_input("\t-Set up the container automatically? [y/N]: ")
				 if inp == "y" or inp == "Y":
						 return True
				 else:
						 print "\t-[ERROR] Cannot run without a container."
						 print "\t-To create a container manually, run as root:"
						 print "\t-\"docker run --cap-add=SYS_ADMIN -d --device=<disk>:/dev/xvda:rw saurabhd04/docker_fio tail -f /dev/null\""
						# print "\t...Exiting! Bye!"
						 exit(1) 
				

## -------------------------------------------------------------------------

