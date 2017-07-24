

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
			exit(1)

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
					exit(1)
		except Exception, e:
			print "\n[ERROR] Something went wrong. Please try again..."
			exit(1)

## -------------------------------------------------------------------------

	# Verify if benchmark container is running
	def verifyFioContainer(self):
		try:
			#print "\t...Verifying if benchmark container is set up"
			res = subprocess.check_output("docker ps | grep docker_fio | wc -l", shell=True)
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
						 print "\t-\"docker run --cap-add=SYS_ADMIN -d --device=/dev/nvme0n1:/dev/xvda:rw saurabhd04/docker_fio tail -f /dev/null\""
						# print "\t...Exiting! Bye!"
						 exit(1) 
				

## -------------------------------------------------------------------------
	
	# Set up a container from image and run as daemon
	def setupBenchmarkContainer(self, num):
		try:
			print "\nSetting up %s container(s) for benchmarking..."%num
			while(1):
				# Takes only valid disk file
				print "\t-Where is your NVMe disk located?"
				res = subprocess.check_output("lsblk | grep disk",shell=True)
				print "\t",
				lines = res.split("\n")
				# display all available disks
				for line in lines:
					if line.split(" ")[0] == "":
							continue
					print "/dev/"+line.split(" ")[0]+"\t",
				print "\n"
				location = raw_input("\t-Enter disk name to benchmark:")

				if os.path.exists(location):
					
					print "\t-[INFO] NVMe disk will be mounted at /dev/xvda inside containers\n"
					containerIds = []
					for i in range(num):
						# spawn containers and mount nvme disk as volume
						cmd = "docker run --cap-add=SYS_ADMIN -d --device="+location+":/dev/xvda:rw saurabhd04/docker_fio tail -f /dev/null"	
						res = subprocess.check_output(cmd, shell=True)
						containerIds.append(res)
						print "\t-Benchmark container #%s is set up"%(i+1)
						print "\t-[INFO] New Container ID:"+res
						#if res == "":
						#	break
					return containerIds 
				else:
					print "\n\t-[ERROR] No such file or directory. NVMe-CLI won't work on HDD."
					op = raw_input("\t-Press \"N\" to quit, any key to continue:")
					if op =="N" or op=="n":
							print "\t-Exiting! Bye!"
							exit(1)
					else:
							continue

		except Exception, e:
			print "\n[ERROR] Something went wrong. Try again!"
			print str(e)
			exit(1)
## -------------------------------------------------------------------------
	
	# Clean up by removing containers
	def cleanup(self, id):
		try:
			while(1):
				inp = raw_input("\nCleanup the environment? [y|N]:")
				if inp == "y" or inp == "Y":
					for id in id:
						#remove containers by docker stop and docker rm
						print "\t-[INFO] Removing container:%s"%id
						cmd = "docker stop "+id+" && docker rm "+id
						res = subprocess.check_output(cmd, shell=True)
					return
				else:
					return
		except Exception, e:
			print "\n[ERROR] Something went wrong. Try again!"
			print str(e)
			exit(1)


## -------------------------------------------------------------------------

	# if jobfile is mentioned, copy that to docker containers
	def copyToDocker(self, ids, jobfile):
		try:
				for id in ids:
					#print "Copying jobfile to containers..."
					cmd = "docker cp "+jobfile+" "+id+":/"
					res = subprocess.check_output(cmd, shell=True)
		except Exception, e:
				print "\n[ERROR] Something went wrong. Try again!"
				print str(e)
				exit(1)

