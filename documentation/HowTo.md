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
  
* Install Docker

  
