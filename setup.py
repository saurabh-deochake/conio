#!/bin/pyton

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

from setuptools import setup


with open('README.md') as f:
	long_description = f.read()

setup(
	name='Conio',
	version='1.0.3',
	description='Conio- A lightweight tool for containerized I/O benchmarking of NVMe-based cloud storage',
	long_description = long_description,
	url = 'https://github.com/saurabh-deochake/conio',
	author='Saurabh Deochake',
	author_email='saurabh.deochake@intel.com',
	license='Apache License, Version 2.0',
	#py_modules=['conio'],
	install_requires=['Click','configparser'],
	entry_points='''
		[console_scripts]
		conio=src.conio:conio
	'''

)
