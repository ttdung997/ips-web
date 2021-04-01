# HostIDPS
Building Host based IDPS for Linux and Windows

# Windows

## Setup environment
This project using `Python 3.8.1` on Windows 10 64 bit
About IDE and Editor: Pycharm, Visual Studio Code, Sublime Text 3
### Create Virtual Environment
`$ cd HostIDPS`

`$ python -m venv venv`

Run project in virtual environment

`$ .\venv\Scripts\activate`

`$ python demo.py`

### On Visual Studio Code

`Error: Cannot be loaded because running scripts is disabled on this system.`

To fix the error, run the command below

`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

Back to step create venv

## Install library for project
### # Install crypto library
`$ pip install pycryptodome`
### # Install API windows event log 
`$ pip install pywin32`

# Linux
### Create Virtual Environment
`$ sudo apt-get installl python3-pip`

`$ sudo pip3 install virtualenv`

`$ cd HostIDPS`

`$ virtualenv -p python3 venv`

Run project in virtual environment

`$ source venv/bin/activate`

Example

`$ python demo.py [-f] -e "C:\Users\Cu Lee\Desktop\Test" "abc"`

`$ python demo.py [-f] -p CONFIRM_DEL -d "C:\Users\Cu Lee\Desktop\Test" "abc"`

## Install library for project
### # Install crypto library
`$ pip install pycrypto`