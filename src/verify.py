

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
	
	# Set up a container from image and run as daemon
	def setupBenchmarkContainer(self, num):
		try:
			print "\nSetting up %s container(s) for benchmarking..."%num
			while(1):
				# Takes only valid disk file
				print "\t-Where is your disk located?"
				res = subprocess.check_output(LSBLK_GREP_DISK,shell=True)
				print "\t",
				lines = res.split("\n")
				# display all available disks
				for line in lines:
					if line.split(" ")[0] == "":
							continue
					print "/dev/"+line.split(" ")[0]+"\t",
				print "\n"
				location = raw_input("\t-Enter disk name to benchmark:")
				if "nvme" not in location:
					inp = raw_input("\t-[WARNING] NVMe-Cli does not work on HDD. Continue? (y|N):")
					if inp.lower() != "y".lower():
						exit(1)
				
				# if file does not exist
				if not os.path.exists(location):
					print "\n\t-[ERROR] No such file or directory"
					op = raw_input("\t-Press \"N\" to quit, any key to try again:")
					if op =="N" or op=="n":
						print "\t-Exiting! Bye!"
						exit(1)
					else:
						continue

				# if the file is not a block device

				if stat.S_ISBLK(os.stat(location).st_mode): 
				
					
					print "\t-[INFO] The disk will be mounted at /dev/xvda inside containers\n"
					containerIds = []
					for i in range(num):
						# spawn containers and mount nvme disk as volume
						cmd = DOCKER_RUN+ " --cap-add=SYS_ADMIN -d --device="+location+":"+CONT_MOUNT+":rw "+ DOCKER_IMAGE_NAME+" tail -f /dev/null"	
						res = subprocess.check_output(cmd, shell=True)
						containerIds.append(res)
						print "\t-Benchmark container #%s is set up"%(i+1)
						print "\t-[INFO] New Container ID:"+res
						#if res == "":
						#	break
					return containerIds, location
				else:    
					print "\n\t-[ERROR] Not a block device"
					op = raw_input("\t-Press \"N\" to quit, any key to try again:")
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
			
				inp = raw_input("Remove container(s)? [y|N]:")
				if inp == "y" or inp == "Y":
					for id in id:
						#remove containers by docker stop and docker rm
						print "\t-[INFO] Removing container:%s"%id
						cmd = DOCKER_STOP+id+" && "+DOCKER_RM+id
						res = subprocess.check_output(cmd, shell=True)
					exit(0)
				else:
					exit(0)
		except Exception, e:
			print "\n[ERROR] Something went wrong. Try again!"
			print str(e)
			exit(1)

## ------------------------------------------------------------------------

	# Clean up by container name or id
	def cleanupSpecific(self, attr):
		try:
		
				cmd = DOCKER_PS_GREP+attr
				if not subprocess.check_output(cmd, shell=True):
					print "\nNo such running container: %s"%attr
					exit(1)
				else:
					inp = raw_input("Remove container? [y|N]:")
					if inp.lower() == 'y'.lower():
						cmd = DOCKER_STOP+attr+" && "+DOCKER_RM+attr
						print "\t- [INFO] Removing contaier:%s"%attr
						res = subprocess.check_output(cmd, shell=True)
						exit(0)
					else:
						exit(0)
		except Exception, e:
			print "\n[ERROR] No such running container: %s"%attr
			exit(1)
## -------------------------------------------------------------------------

	# if jobfile is mentioned, copy that to docker containers
	def copyToDocker(self, ids, jobfile):
		try:
				for id in ids:
					#print "Copying jobfile to containers..."
					cmd = DOCKER_CP+jobfile+" "+id+":/"
					res = subprocess.check_output(cmd, shell=True)
		except Exception, e:
				print "\n[ERROR] Something went wrong. Try again!"
				print str(e)
				exit(1)
## --------------------------------------------------------------------------
   
    # Get the IDs of containers running
   	def getContainerID(self, num):
		try:
			containerIDs = []
			# check if docker container with specific image is running
			res = subprocess.check_output(DOCKER_PS_GREP+" "+DOCKER_IMAGE_NAME,shell=True)
			#gather ids for all containers
			for cont in res.split("\n"):
				id = cont.split(" ")[0]
				if id:
					containerIDs.append(cont.split(" ")[0])
					return containerIDs
		except Exception, e:
			print "\nNothing to clean"
			exit(1)

