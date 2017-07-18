

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
import subprocess
import sys; sys.dont_write_bytecode = True

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
			res = subprocess.check_output("rpm -qa | grep docker", shell=True)
			if res == "":
					print "\t-[ERROR] Is Docker installed? Please install Docker..."
					return False
			else:
					return True
		except Exception, e:
			print "\t-[ERROR] Is Docker installed? Please install Docker..."
			print "\t-"+str(e)

## -------------------------------------------------------------------------
	# Verify if Docker daemon is running
	def verifyDockerdRunning(self):
		try:
			#print "\t...Verifying Docker daemon"
			res = subprocess.check_output("ps -ef | grep dockerd", shell=True)
			if "/usr/bin/dockerd" in res:
					return True
			else:
					print "\t-[ERROR] Docker daemon is not running"
					return False
		except Exception, e:
			print "\n[ERROR] Something went wrong. Please try again..."
			print str(e)

## -------------------------------------------------------------------------

	# Verify if benchmark container is running
	def verifyFioContainer(self):
		try:
			#print "\t...Verifying if benchmark container is set up"
			res = subprocess.check_output("docker ps | grep docker_fio | wc -l", shell=True)
			
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
			return res
		except Exception, e:
				 print "\t-[ERROR] Benchmark container is not running"
				 inp = raw_input("\t-Set up the container automatically? [y/N]: ")
				 if inp == "y" or inp == "Y":
						 return True
				 else:
						 print "\t-[ERROR] Cannot run without a container."
						 print "\t-To create a container manually, run as root:"
						 print "\t-\"docker run --cap-add=SYS_ADMIN -d --device=/dev/nvme0n1:/dev/xvda:rw saurabhd04/docker_fio tail -f /dev/null\""
						# print "\t...Exiting! Bye!"
						 exit(1) 
				

## -------------------------------------------------------------------------
	
	# Set up a container from image and run as daemon
	def setupBenchmarkContainer(self, num):
		try:
			print "\nSetting up %s container(s) for benchmarking..."%num
			while(1):
				location = raw_input("\t-Where is your NVMe disk located?: ")
				if os.path.exists(location) and ("/dev/nvme".lower() in location):
					containerIds = []
					for i in range(num):
						cmd = "docker run --cap-add=SYS_ADMIN -d --device="+location+":/dev/nvme0n1:rw saurabhd04/docker_fio tail -f /dev/null"	
						res = subprocess.check_output(cmd, shell=True)
						containerIds.append(res)
						print "\t-Benchmark container #%s is set up"%(i+1)
						print "\t-[INFO] New Container ID:"+res
						#if res == "":
						#	break
					
					return containerIds
				else:
					print "\t-[ERROR] No such file or directory"
					op = raw_input("\t-Press \"N\" to quit, any key to continue:")
					if op =="N" or op=="n":
							print "\t-Exiting! Bye!"
							exit(1)
					else:
							continue

		except Exception, e:
			print "\n[ERROR] Something went wrong. Try again!"
			print str(e)
## -------------------------------------------------------------------------
	
	# Clean up by removing containers
	def cleanup(self, id):
		try:
			for id in id:
				print "\nRemoving container:%s"%id
				cmd = "docker stop "+id+" && docker rm "+id
				res = subprocess.check_output(cmd, shell=True)
		except:
			print "\n[ERROR] Something went wrong. Try again!"
			print str(e)







