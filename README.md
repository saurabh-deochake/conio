# conio ![](https://travis-ci.com/saurabh-deochake/conio.svg?token=RxYsxYxhaD6syK9zknyr&branch=master) ![](https://nodesecurity.io/orgs/saurabh-github/projects/140144bd-6f3f-40cc-9211-0c5d5a99b362/badge) [![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badge/)    

A command line tool for automatic containerized I/O benchmarking of cloud storage.     
Copyright Intel Corporation. 2017.

#### Releases
* [Conio v1.0.0](https://github.com/saurabh-deochake/conio/releases/tag/v1.0.0)

#### Current status    
beta testing       

#### Features
* Launch specified number of Docker containers automatically     
* Supports FIO benchmarking    
* Support for NVMe-Cli Master for NVMe storage      

#### Usage
* Get Conio source from GitHub    
`git clone https://github.com/saurabh-deochake/conio.git`

* Install on your system    
`python setup.py install`

```
# conio --help
Usage: conio [OPTIONS] COMMAND [ARGS]...

  Conio- A lightweight tool for containerized I/O benchmarking of NVMe SSDs
  Copyright Intel Corporation. 2017.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  clean   Stop and remove containers
  create  Create and launch containers
  run     Run tools inside containers
```

```    
# conio run --help
Usage: conio run [OPTIONS]

Run tools inside containers

Options:
  --tool [fio|nvme|all]           I/O benchmark tools to run: fio/nvme/all
                                  (both: default)
  --num INTEGER                   Number of containers to benchmark
  --thread TEXT                   Run jobs as threads
  --direct TEXT                   Force Direct I/O
  --group_reporting TEXT          Get consolidated result for all job
                                  threads/processes
  --ioengine [libaio|sync]        I/O engine for the I/O operations for the
                                  jobs
  --size TEXT                     Total size of I/O operations benchmarking
  --do_verify TEXT                Run the verify phase after a write phase
  --time_based TEXT               Run time based I/O benchmark tests
  --cpus_allowed_policy TEXT      Set CPU affinity for the job
  --iodepth TEXT                  Set IODepth for this job
  --rw [randread|randwrite|read|write]
                                  Run sequential/random read and/or operations
  --blocksize TEXT                Set the blocksize for this job
  --runtime TEXT                  Time (in minutes) this job will run for
  --numjobs TEXT                  Number of jobs to carry out benchmarking
  --name TEXT                     Name for your job
  --jobfile TEXT                  Path to your fio job file
  --config TEXT                   Path to config file for mixed jobs benchmark
  --mixed_jobs                    Set this if you want to run different jobs
                                  on containers. (A config file is required)
  --help                          Show this message and exit.
```
### Example
* Create    
```
$ conio create --num=2

Setting up 2 container(s) for benchmarking...
        -Where is your NVMe disk located?
        /dev/sda        /dev/sdb        /dev/nvme0n1

        -Enter disk name to benchmark:/dev/sda
        -[WARNING] NVMe-Cli does not work on HDD. Continue? (y|N):y
        -[INFO] NVMe disk will be mounted at /dev/xvda inside containers

        -Benchmark container #1 is set up
        -[INFO] New Container ID:1aa125a86b4f2e429c294a6d39828a34bed39fa63da0645b10f56c55c5f9d46f

        -Benchmark container #2 is set up
        -[INFO] New Container ID:6e157f6c2a57355d22037a6d7bdcd216d6918b6faeb78f48edd44d849b101c43

```    

* Run
```
$ conio run --num=2 --tool=fio

Conio- A lightweight tool for containerized I/O benchmarking of NVMe SSDs
Intel Corporation. 2017.

Verifying Docker enviroment...
        -[INFO] Docker container for benchmarking already set up

Setting up 1 container(s) for benchmarking...
        -Where is your NVMe disk located?
        /dev/sda        /dev/sdb        /dev/nvme0n1

        -Enter disk name to benchmark:/dev/nvme0n1
        -[INFO] NVMe disk will be mounted at /dev/xvda inside containers

        -Benchmark container #1 is set up
        -[INFO] New Container ID:6226f32e98d7af0affc4bb38a55e89211f64abf59e664756d10602763619f53e


Go grab some coffee while I finish benchmarking your containers!

Now running Fio inside containers...
        -Inside container:6226f32e98d7
        -Inside container:90875dc7b1ea

Summary for container:6226f32e98d7
Operation:randread
Jobs:4
Blocksize:4K
Iodepth:32
IOPS:165710
Bandwidth:662841KB/s
Avg Latency:760.18 usec
99.99 Latency: 4832 usec

Summary for container:90875dc7b1ea
Operation:randread
Jobs:4
Blocksize:4K
Iodepth:32
IOPS:156134
Bandwidth:624538KB/s
Avg Latency:808.54 usec
99.99 Latency: 4960 usec
```
* Clean
```
# conio clean

Cleanup the environment? [y|N]:y
        -[INFO] Removing container:6226f32e98d7
        -[INFO] Removing container:90875dc7b1ea
```
### Contributing
If you are interested in becoming a contributer to this project, then please fork the project. As this project is in alpha testing, some things may break. Please create an issue on the repo if you find something broken. 

### License
The tool is made avaiable under Apache 2.0 license. Please read the terms of license located in LICENSE file.

### Author
The tool conio was written by [Saurabh Deochake](https://saurabh-deochake.github.io) for Intel Corporation. 


