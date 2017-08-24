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

from setuptools import setup

DESCRIPTION = 'Conio- A lightweight tool for containerized I/O benchmarking \
of NVMe-based cloud storage'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='conio',
    version='1.0.4',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/saurabh-deochake/conio',
    author='Saurabh Deochake',
    author_email='saurabh.deochake@intel.com',
    license='Apache License, Version 2.0',
    install_requires=['Click', 'configparser', 'ascii_graph'],
    entry_points='''
          [console_scripts]
          conio=conio.src.conio:conio
    '''
)
