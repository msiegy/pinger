import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from subprocess import Popen, PIPE
from netmiko import Netmiko
from getpass import getpass
from time import sleep

host=input("enter target ping IP: ")
#count=input("enter ping failure count: ")
switch=input("enter switch IP: ")
username=input("enter username: ")
#password=input("enter password: ")
password = getpass()
failure=0

def pinger2(host):
    cmd = "ping.exe " + host + " -n 1"
    output = subprocess.Popen(cmd,stdout = subprocess.PIPE).communicate()[0]

    print(output)
    output = str(output)

    if ('unreachable' in output):
        print("Unreachable")
        return False
    elif ('timed' in output):
        print("TimeOut")
        return False
    else:
        print("Success")
        return True

#Continue ping until we see 5 failures.
while(True):
     if(pinger2(host)):
        failure = 0
        sleep(1)
     else:
        failure = failure + 1
        print("add 1 to failure" , failure)
     if(failure > 3):
        break

print('\n#####\n Ping Failed, execute switch commands\n#####\n')

device = {
    "device_type": "cisco_xe",
    "ip": switch,
    "username": username,
    "password": password,
    "secret": password,
}

connect = Netmiko(**device)
"""Enter switch commands here"""
print(connect.send_command("show mod"))
connect.enable()
print(connect.send_command("event manager run adj_fail"))
connect.disconnect
