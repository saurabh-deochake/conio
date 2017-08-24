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


## File which stores all global variables

## ----------------IMPORTANT NOTE------------------------##
## Please leave a space after you define your variable.  ##
## Failure to do so may cause fatal misbehavior.         ##
##                Proceed with caution!                  ##

# Docker commands
DOCKER_PS = "docker ps "
DOCKER_PS_ALL = "docker ps -a "
DOCKER_PS_GREP = "docker ps | grep "
DOCKER_PS_STOPPED = "docker ps -f \"status=exited\" "
DOCKER_EXEC = "docker exec "
DOCKER_RUN = "docker run "
DOCKER_STOP = "docker stop "
DOCKER_RM = "docker rm "
DOCKER_CP = "docker cp "
DOCKER_START = "docker start "

# System commands
GREP = " | grep "
GREP_EXACT = " | grep -w "
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
