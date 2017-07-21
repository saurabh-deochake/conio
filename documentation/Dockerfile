

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

 

