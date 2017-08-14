#!/bin/python

"""
http://www.apache.org/licenses/LICENSE-2.0.txt
Copyright 2017 Intel Corporation

Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

Author: Saurabh Deochake, Intel Corporation
"""

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
