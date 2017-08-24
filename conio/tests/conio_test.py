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


### Build testing script

import sys
import subprocess

# This addition to PYTHONPATH is very specific to travis build.
# Please change the path to appropriate /path/to/your/subpackage
# for proper resolution and import of packages

sys.path.append('/home/travis/build/saurabh-deochake/conio/conio/src')

from config import RPM_GREP, PS_GREP, DOCKER_PS_GREP, DOCKER_IMAGE_NAME

def test_docker():
    """
    Test to check if docker and docker daemon is running
    """
    try:
        print "\nVerifying Docker enviroment..."
        res = subprocess.check_output(RPM_GREP+" docker", shell=True)
        if res == "":
            print "\t-[ERROR] Is Docker installed? Please install Docker..."
        print "\t...Verifying Docker daemon"
        res = subprocess.check_output(PS_GREP+" dockerd", shell=True)
        if "/usr/bin/dockerd" in res:
            print "\t-[INFO] Docker daemon is running"
        else:
            print "\t-[ERROR] Docker daemon is not running"

        print "\t...Verifying if benchmark container is set up"
        res = subprocess.check_output(DOCKER_PS_GREP+DOCKER_IMAGE_NAME+"| wc -l",\
                                        shell=True)

        exit(0)


    except Exception, exception:
        print "\n[ERROR] Something went wrong. Stack trace:"
        print str(exception)
        exit(0)

def test_run_container():
    """
    Skeleton code to test if container is running
    """
    try:
        pass

    except Exception, exception:
        print "\n[ERROR] Something went wrong. Stack trace:"
        print str(exception)

test_docker()
test_run_container()
