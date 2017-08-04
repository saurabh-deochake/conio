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

## File which stores all global variables

## --NOTE--: Please leave a space after you define your variable. 
## Failure to do so may cause in misbehavior. Proceed with caution!

# Docker commands
DOCKER_PS = "docker ps "
DOCKER_PS_GREP = "docker ps | grep "
DOCKER_EXEC = "docker exec "
DOCKER_RUN = "docker run "
DOCKER_STOP = "docker stop "
DOCKER_RM = "docker rm "
DOCKER_CP = "docker cp "

# System commands
RPM_GREP = "rpm -qa | grep "
PS_GREP = "ps -ef | grep "
LSBLK_GREP_DISK = "lsblk | grep disk"

# Tools
FIO = "fio "
NVME = "nvme "
FIO_OUT = "/fio.out "
NVME_OUT = "/nvme.out "

## Other

# Mount point inside containers
CONT_MOUNT = "/dev/xvda" ## CAUTION: Setting it to /dev/nvme0n1 doesn't work

# Docker Image
DOCKER_IMAGE_NAME = "saurabhd04/docker_fio"

