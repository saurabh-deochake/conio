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

#Download base image from Centos
FROM centos:latest

#Maintainer 
MAINTAINER Saurabh Deochake

#Set environment variables
ENV http_proxy http://proxy.jf.intel.com:911

#Run packages required
#RUN yum -y groupinstall "Development tools"
RUN yum -y install libaio librados2-devel qemu-kvm qemu-kvm-tools qemu-img

#ADD FIO and NVMe-CLI 
ADD fio-2.2.10-1.el7.x86_64.rpm /
ADD nvme-cli-0.7-1.el7.x86_64.rpm /

#Install FIO and NVMe-CLI

#1-FIO
RUN rpm -ivh /fio-2.2.10-1.el7.x86_64.rpm

#2-NVMe-CLI
RUN rpm -ivh /nvme-cli-0.7-1.el7.x86_64.rpm

 

