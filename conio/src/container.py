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


import os
import subprocess
import stat

from config import *

class Container(object):
    """
    Manage all Docker container related operations.
    Extends: none
    """

    def __init__(self):
        """
        class object constructor.
        """
        pass

    # Set up a container from image and run as daemon
    def setup_benchmark_container(self, num):
        """
        Sets up Docker containers required for benchmarks

        :param num: Total number of Docker containers to spawn
        :returns: Ids of containers created, location of disk drive to benchmark
        :raises Exception: if command fails to execute
        """
        try:
            print "\nSetting up %s container(s) for benchmarking..."%num
            while 1:
                #takes only valid disk file
                print "\t-Where is your disk located?"
                res = subprocess.check_output(LSBLK_GREP_DISK, shell=True)
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
                    op_value = raw_input("\t-Press \"N\" to quit, any key to try again:")
                    if op_value == "N" or op_value == "n":
                        print "\t-Exiting! Bye!"
                        exit(1)
                    else:
                        continue

                # if the file is not a block device
                if stat.S_ISBLK(os.stat(location).st_mode):
                    print "\t-[INFO] The disk will be mounted at /dev/xvda inside containers\n"
                    container_ids = []
                    for i in range(num):
                        # spawn containers and mount nvme disk as volume
                        cmd = DOCKER_RUN+ " --cap-add=SYS_ADMIN -d --device="+\
                              location+":"+CONT_MOUNT+":rw "+\
                              DOCKER_IMAGE_NAME+" tail -f /dev/null"
                        res = subprocess.check_output(cmd, shell=True)
                        container_ids.append(res)
                        print "\t-Benchmark container #%s is set up"%(i+1)
                        print "\t-[INFO] New Container ID:"+res
                    return container_ids, location
                else:
                    print "\n\t-[ERROR] Not a block device"
                    op_value = raw_input("\t-Press \"N\" to quit, any key to try again:")
                    if op_value == "N" or op_value == "n":
                        print "\t-Exiting! Bye!"
                        exit(1)
                    else:
                        continue

        except subprocess.CalledProcessError, exception:
            print "\n[ERROR] Something went wrong. Try again!"
            print str(exception)
            exit(1)
## -------------------------------------------------------------------------

    # Clean up by removing containers
    def cleanup(self, container_ids):
        """
        Stop and remove containers used for benchmarking.

        :param id: list of all container ids
        :returns: exit gracefully when done
        :raises Exception: if command fails to execute
        """
        try:
            inp_value = raw_input("Remove container(s)? [y|N]:")
            if inp_value == "y" or inp_value == "Y":
                for id_value in container_ids:
                    #remove containers by docker stop and docker rm
                    print "\t-[INFO] Removing container:%s"%id_value
                    cmd = DOCKER_STOP+id_value+" && "+DOCKER_RM+" -v "+id_value
                    subprocess.check_output(cmd, shell=True)
                exit(0)
            else:
                exit(0)

        except subprocess.CalledProcessError, exception:
            print "\n[ERROR] Something went wrong. Try again!"
            print str(exception)
            exit(1)
## -------------------------------------------------------------------------

    # clean up by container name or id
    def cleanup_specific(self, attr):
        """
        Stop and remove a specific container.

        :param attr: string id/name to remove container by name/id
        :returns: exit gracefully when done
        :raises Exception: if command fails to execute
        """
        try:
            cmd = DOCKER_PS_GREP+attr
            if not subprocess.check_output(cmd, shell=True):
                print "\nNo such running container: %s"%attr
                exit(1)
            else:
                inp_value = raw_input("Remove container? [y|N]:")
                if inp_value.lower() == 'y'.lower():
                    cmd = DOCKER_STOP+attr+" && "+DOCKER_RM+" -v "+attr
                    print "\t- [INFO] Removing contaier:%s"%attr
                    subprocess.check_output(cmd, shell=True)
                    exit(0)
                else:
                    exit(0)
        except subprocess.CalledProcessError:
            print "\n[ERROR] No such running container: %s"%attr
            exit(1)

## ------------------------------------------------------------------------

    # if jobfile is mentioned, copy that to docker containers
    def copy_to_docker(self, container_ids, jobfile):
        """
        Copy FIO jobfile to containers.

        :param ids: list of ids of all containers
        :param jobfile: location of fio jobfile
        :returns: nothing
        :raises Exception: if command fails to execute
        """
        try:
            for id_value in container_ids:
                #print "Copying jobfile to containers..."
                cmd = DOCKER_CP+jobfile+" "+id_value+":/"
                subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError, exception:
            print "\n[ERROR] Something went wrong. Try again!"
            print str(exception)
            exit(1)
## -------------------------------------------------------------------------

    # Get the IDs of containers running
    def get_container_id(self, num):
        """
        Get ids of all running containers.

        :param num: number of ids to get
        :returns: list of container ids
        :raises Exception: if command fails to execute
        """
        try:
            container_ids = []
            #check if docker container with specific image is running
            res = subprocess.check_output(DOCKER_PS_GREP+" "+DOCKER_IMAGE_NAME,\
                  shell=True)
            #gather ids for all containers
            for cont in res.split("\n"):
                id_value = cont.split(" ")[0]
                if id_value:
                    container_ids.append(cont.split(" ")[0])
            return container_ids
        except subprocess.CalledProcessError:
            print "\nNo containers found"
            exit(1)


## -------------------------------------------------------------------------

    # Get details of containers running/stopped
    def list_containers(self, running):
        """
        list all running or stopped containers.

        :param running: int value to show if running or stopped is needed
        :returns: dictionary of container id and name
        :raises Exception: if command fails to run
        """
        try:
            if running:
                res = subprocess.check_output(DOCKER_PS_GREP+" "+DOCKER_IMAGE_NAME,\
                                                shell=True)
                if not res:
                    print "\nNo running container found. Aborting"
                    exit(1)
            if not running:
                res = subprocess.check_output(DOCKER_PS_STOPPED+GREP+DOCKER_IMAGE_NAME,\
                                                shell=True)
                if not res:
                    print "\nNo container found. Aborting"
                    exit(1)
            #gather all containers
            data = {}
            for containers in res.split("\n"):
                cont = containers.split()
                if not cont:
                    break
                data[cont[0]] = cont[-1]

            return data

        except subprocess.CalledProcessError:
            print "\nNo running/stopped container found. Aborting!"
            exit(1)

## --------------------------------------------------------------------------

    # Stop containers for later use
    def stop_containers(self, attr):
        """
        stop all containers for future use.

        :param attr: string representing either id or name of container
        :returns: exit gracefully when done
        :raises Exception: if command fails to execute
        """
        try:
            if type(attr) is list:
                inp = raw_input("Stop container(s)? [y|N]:")
                if inp.lower() == "y".lower():
                    for id_value in attr:
                        # stop all containers
                        print "\t-[INFO] Stopping container:%s"%id_value
                        subprocess.check_output(DOCKER_STOP+id_value, shell=True)
                    exit(0)
                else:
                    exit(0)
            else:
                cmd = DOCKER_PS_ALL+GREP_EXACT+attr
                if not subprocess.check_output(cmd, shell=True):
                    print "\nNo such container: %s"%attr
                    exit(1)
                else:
                    print "\t-[INFO] Stopping container:%s"%attr
                    subprocess.check_output(DOCKER_STOP+attr, shell=True)

        except subprocess.CalledProcessError:
            print "\n[ERROR] No such container found"
            exit(1)

## -------------------------------------------------------------------------

    # Start already stopped containers
    def start_containers(self, attr):
        """
        start container(s) for benchmarking.

        :param attr: list/string containing all ids/specific name
        :returns: nothing
        :raises Exception: if command fails to execute
        """
        try:
            if type(attr) is list:
                for id_value in attr:
                    #start each container one by one
                    print "\t-[INFO] Starting container:%s"%id_value
                    subprocess.check_output(DOCKER_START+id_value, shell=True)
                exit(0)
            else:
                cmd = DOCKER_PS_ALL+GREP_EXACT+attr
                if not subprocess.check_output(cmd, shell=True):
                    print "\nNo such container: %s"%attr
                    exit(1)
                else:
                    print "\t-[INFO] Staring container:%s"%attr
                    subprocess.check_output(DOCKER_START+attr, shell=True)
        except subprocess.CalledProcessError:
            print "\n[ERROR] No such container found"
            exit(1)
