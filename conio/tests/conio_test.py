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

#from __future__ import absolute_import
import sys
sys.path.append('../src')

from verify import Verify


#import src.runtime as runtime

def test_docker():
	try:
		verify = Verify()
		res =verify.verifyEnvironment()

		if not res:
			print "\n Docker is set up and daemon is running"


	except Exception, e:
		print "\n[ERROR] Something went wrong. Stack trace:"
		print str(e)


def test_runContainer():
	try:
		
		pass

	except Exception, e:
		print "\n[ERROR] Something went wrong. Stack trace:"
		print str(e)

test_docker()
test_runContainer()

