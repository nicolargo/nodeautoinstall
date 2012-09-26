====================================================
NodeJS and NPM installation script for Debian Stable
====================================================


## Description

NodeJS and NPM are only available in Debian Sid.

Here is a simple Python script for:

* Download and install the latest [NodeJS](https://github.com/joyent/node) version
* Download and install [NPM](https://github.com/isaacs/npm)

That's all folks !

### How to process ?

In a console/terminal of you Debian distribution, enter the following commands:

      $ cd /tmp

      $ git clone git://github.com/nicolargo/nodeautoinstall.git
      $ cd nodeautoinstall
      or
      $ wget https://raw.github.com/nicolargo/nodeautoinstall/master/nodeautoinstall.py

      $ sudo python ./nodeautoinstall.py

### Result

![screenshot](https://github.com/nicolargo/nodeautoinstall/raw/master/screenshot.png)

