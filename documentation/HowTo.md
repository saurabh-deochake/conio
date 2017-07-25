### Setting up Conio on your system
This is a step-by-step guide to setup conio on your system. The tutorial also discusses potential problems and how to fix them. 

* **Proxy Setting**   
If you are sitting behind a proxy, then you have to change a few settings, environment variables and make configuration files 
to make sure our set up runs smooth.

  * `http_proxy` variable    
  Set up `http_proxy` environment variable to your proxy url.    
  
  ```
   $ export http_proxy="http://proxy.something.com:port"    
   $ expoty https_proxy="https://proxy.something.com:port"
  ```

  * Git behind proxy   
  Next, we have to set up `http_proxy` for git for smoothly downloading and installing conio through source code. Run the command    
  `$ git config --global http.proxy http://proxy.something.com:port`
  
  * Yum behind proxy
  To install conio on your system, we need Python's pip installer. We need to make some changes to `/etc/yum.conf` so that yum works behind a proxy. Run following commands to make sure your package installer works behind the proxy.    
  
  ```
  $ vi /etc/yum.conf
  
  [main]
  ...
  ...
  proxy=http://proxy.something.com:port
  ...
  ```
  
* **Docker**
 In order to run the tool, it is mandatory that we have Docker installed and docker service is enabled and running.    
  * Install Docker    
  Install the latest version of Docker using yum.   
  
  `$sudo yum -y install docker`
  
  * Start Docker service
  Now that Docker is installed, let's start docker service using    
  `$ systemctl start docker`
  
  * Proxy for Docker
  The tool pulls the image from `saurabhd04/docker_fio` in order to launch the containers and run I/O benchmarking inside. Therefore, in order for `docker pull` to be successful, we must mention proxy settings for Docker. Run following commands for Docker behind proxy:    
  
  ```
  $ mkdir /etc/systemd/system/docker.service.d
  $ vi /etc/systemd/system/docker.service.d/http-proxy.conf
  
  [Service]
  Environment="HTTP_PROXY=http://proxy.something.com:port/"
  
  $ sudo systemctl daemon-reload
  $ sudo systemctl restart docker
  ```
  Now, your Docker environment is set up.
  
* **Python Pip Installer**
  We use Pip installer to install the tool on to a system. So, if you do not already have pip installed, install it using yum. For CentOS, the package `python-pip` is available in EPEL repository. So, please download epel repo and then install pip.   
  
  ```
  $ sudo yum --enablerepo=extras install epel-release
  $ sudo yum -y install python-pip
  ```
  
* **Installing conio**
  Now, 
  

  
