

#!/bin/python

import subprocess

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

class Dockerbench:
	def __init__(self):
		# check environment variable
		if self.verifyDocker():
				if self.verifyDockerdRunning():
						if self.verifyFioContainer():
							self.setupBenchmarkContainer()
						else:
							print "Docker container for benchmarking already set up...\n\n"
						#exit(1)

## --------------------------------------------------------------------------

	# Verify if docker is installed
	def verifyDocker(self):
		try:
			print "Verifying Docker enviroment..."
			res = subprocess.check_output("rpm -qa | grep docker", shell=True)
			if res == "":
					print "Is Docker installed? Please install Docker..."
					return False
			else:
					return True
		except Exception, e:
			print "docker Something went wrong. Please try again..."
			print str(e)

## -------------------------------------------------------------------------
	# Verify if Docker daemon is running
	def verifyDockerdRunning(self):
		try:
			print "Verifying Docker daemon..."
			res = subprocess.check_output("ps -ef | grep dockerd", shell=True)
			if "/usr/bin/dockerd" in res:
					return True
			else:
					print "Docker daemon is not running..."
					return False
		except Exception, e:
			print "dockerd Something went wrong. Please try again..."
			print str(e)

## -------------------------------------------------------------------------

	# Verify if benchmark container is running
	def verifyFioContainer(self):
		try:
			print "Verifying if benchmark container is set up..."
			res = subprocess.check_output("docker ps | grep docker_fio", shell=True)
			
			## DO SOMETHING WITH THIS RES
			"""print res
			if res.stdout == "":
					print "Benchmark container is not running..."
					inp = raw_input("Do you want to set up the container \
									automatically? y/N")
					if inp == "N" or inp == "n":
						return false
					elif inp == "y" or inp == "Y":
						return setupBenchmarkContainer()"""
			return
		except Exception, e:
				 print "Benchmark container is not running..."
				 inp = raw_input("Do you want to set up the container automatically? y/N ")
				 if inp == "N" or inp == "n":
						 return False 
				 elif inp == "y" or inp == "Y":
						return True
				#print str(e)

## -------------------------------------------------------------------------
	
	# Set up a container from image and run as daemon
	def setupBenchmarkContainer(self):
		try:
			print "Setting up a container for benchmarking...\n"
			print "Make sure you have NVMe disk at /dev/nvme0n1..\n."
			cmd = "docker run --cap-add=SYS_ADMIN -d --device=/dev/nvme0n1:/dev/xvda:rw saurabhd04/docker_fio tail -f /dev/null"	
			res = subprocess.check_output(cmd, shell=True)
			print res
			if res != "":
				return True
			#return True
		except Exception, e:
			print str(e)
## -------------------------------------------------------------------------

if __name__ == '__main__':
	d = Dockerbench()


		
		
