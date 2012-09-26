#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to install NodeJS + NPM on Debian Stable Version
#
# Why ?
# Because NodeJS is only available in Sid...
#
# Nicolargo (aka) Nicolas Hennion
# http://www.nicolargo.com
# 09/2012
#

"""
Install NodeJS and NPM on Debian Stable
"""

import os, sys, platform, getopt, shutil, logging, getpass
from select import select

# Global variables
#-----------------------------------------------------------------------------

_VERSION="1.0"
_DEBUG = 0
_LOG_FILE = "/tmp/nodeautoinstall.log"
_DEFAULT_PATH = "/opt/node"

# Classes
#-----------------------------------------------------------------------------

class colors:
	RED = '\033[91m'
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	ORANGE = '\033[93m'
	NO = '\033[0m'

	def disable(self):
		self.RED = ''
		self.GREEN = ''
		self.BLUE = ''
		self.ORANGE = ''
		self.NO = ''

# Functions
#-----------------------------------------------------------------------------

def init():
	"""
	Init the script
	"""
	# Globals variables
	global _VERSION
	global _DEBUG

	# Set the log configuration
	logging.basicConfig(
		filename=_LOG_FILE,
		level=logging.DEBUG,
		format='%(asctime)s %(levelname)s - %(message)s',
	 	datefmt='%d/%m/%Y %H:%M:%S',
	 )

def syntax():
	"""
	Print the script syntax
	"""
	version()
        print "Goal: Install NodeJS and NPM on a Debian Stable system"
        print "Syntax: "
        print " -h: Display the help message and exit"
        print " -v: Display the version and exit"
        print " -d: Run the script in debug mode (log in the "+_LOG_FILE+" file)"
        print " -o PATH: Set the installation PATH (default is "+_DEFAULT_PATH+")"

def version():
	"""
	Print the script version
	"""
	sys.stdout.write ("NodeAutoInstall version %s" % _VERSION)
	sys.stdout.write (" (running on %s %s)\n" % (platform.system() , platform.machine()))

def isroot():
	"""
	Check if the user is root
	Return TRUE if user is root
	"""
	return (os.geteuid() == 0)

def showexec(description, command, exitonerror = 0, presskey = 0, waitmessage = ""):
	"""
	Exec a system command with a pretty status display (Running / Ok / Warning / Error)
	By default (exitcode=0), the function did not exit if the command failed
	"""

	if _DEBUG: 
		logging.debug ("%s" % description)
		logging.debug ("%s" % command)

	# Wait message
	if (waitmessage == ""):
		waitmessage = description

	# Manage very long description
	if (len(waitmessage) > 65):
		waitmessage = waitmessage[0:65] + "..."
	if (len(description) > 65):
		description = description[0:65] + "..."
		
	# Display the command
	if (presskey == 1):
		status = "[ ENTER ]"
	else:	
		status = "[Running]"
	statuscolor = colors.BLUE
	sys.stdout.write (colors.NO + "%s" % waitmessage + statuscolor + "%s" % status.rjust(79-len(waitmessage)) + colors.NO)
	sys.stdout.flush()

	# Wait keypressed (optionnal)
	if (presskey == 1):
		try:
			input = raw_input
		except: 
			pass
		raw_input()

	# Run the command
	returncode = os.system ("/bin/sh -c \"%s\" >> /dev/null 2>&1" % command)
	
	# Display the result
	if returncode == 0:
		status = "[  OK   ]"
		statuscolor = colors.GREEN
	else:
		if exitonerror == 0:
			status = "[Warning]"
			statuscolor = colors.ORANGE
		else:
			status = "[ Error ]"
			statuscolor = colors.RED

	sys.stdout.write (colors.NO + "\r%s" % description + statuscolor + "%s\n" % status.rjust(79-len(description)) + colors.NO)

	if _DEBUG: 
		logging.debug ("Returncode = %d" % returncode)

	# Stop the program if returncode and exitonerror != 0
	if ((returncode != 0) & (exitonerror != 0)):
		if _DEBUG: 
			logging.debug ("Forced to quit")
		exit(exitonerror)

def getpassword(description = ""):
	"""
	Read password (with confirmation)
	"""
	if (description != ""): 
		sys.stdout.write ("%s\n" % description)
		
	password1 = getpass.getpass("Password: ");
	password2 = getpass.getpass("Password (confirm): ");

	if (password1 == password2):
		return password1
	else:
		sys.stdout.write (colors.ORANGE + "[Warning] Password did not match, please try again" + colors.NO + "\n")
		return getpassword()

def getstring(message = "Enter a value: "):
	"""
	Ask user to enter a value
	"""
	try:
		input = raw_input
	except: 
		pass
	return raw_input(message)

def waitenterpressed(message = "Press ENTER to continue..."):
	"""
	Wait until ENTER is pressed
	"""
	try:
		input = raw_input
	except: 
		pass
	raw_input(message)
	return 0
		
def main(argv):
	"""
	Main function
	"""
	try:
           opts, args = getopt.getopt(argv, "hvdo:", ["help", "version", "debug", "output"])
	except getopt.GetoptError:
		syntax()
		exit(2)

	output_path = _DEFAULT_PATH

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			syntax()
			exit()
		elif opt == '-v':
			version()
			exit()
		elif opt == '-d':
			global _DEBUG
			_DEBUG = 1
                elif opt == '-o':
	                output_path = arg

        showexec ("Install pre-requisites", "apt-get install g++")
        showexec ("Download NodeJS", "rm -rf ~/nodeautoinstall.files && mkdir -p ~/nodeautoinstall.files && cd ~/nodeautoinstall.files && wget -N http://nodejs.org/dist/node-latest.tar.gz")
        showexec ("Install NodeJS", "cd ~/nodeautoinstall.files && tar zxvf node-latest.tar.gz && cd ~/nodeautoinstall.files/node-v* && ./configure --prefix="+output_path+" && make install")
        # showexec ("Add PATH to current username", "echo 'export PATH=$PATH:"+output_path+"/bin' >> ~/.profile")
        # showexec ("Add NODE_PATH to current username", "echo 'export NODE_PATH="+output_path+":"+output_path+"/lib/node_modules' >> ~/.profile")
        showexec ("Install NPM", "curl http://npmjs.org/install.sh | sh -c 'export PATH=$PATH:"+output_path+"/bin ; export NODE_PATH="+output_path+":"+output_path+"/lib/node_modules'")

        print "Optionnaly, add the following lines to your .profile file:"
        print "# --- NodeJS" 
        print "export PATH=$PATH:"+output_path+"/bin"
        print "export NODE_PATH="+output_path+":"+output_path+"/lib/node_modules"
        print "# ---" 

	
# Main program
#-----------------------------------------------------------------------------

if __name__ == "__main__":
	init()
	main(sys.argv[1:])
	exit()
