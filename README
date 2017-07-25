# conio
A command line tool for automatic containerized I/O benchmarking of Docker containers.

#### Current status    
alpha testing       

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
$ conio --help
Usage: conio [OPTIONS]

Options:
  --tool [fio|nvme|all]           I/O benchmark tools to run: fio/nvme/all
                                  (both: default)
  --num INTEGER                   Number of containers to spawn for
                                  benchmarking
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
