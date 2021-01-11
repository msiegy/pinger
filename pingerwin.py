import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from subprocess import Popen, PIPE
from netmiko import Netmiko
from getpass import getpass

host=input("enter target ping IP: ")
#count=input("enter ping failure count: ")
switch=input("enter switch IP: ")
username=input("enter username: ")
#password=input("enter password: ")
password = getpass()
failure=0

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def pinger(num, wait, host):
    ping = Popen("ping -n {} -w {} {}".format(num, wait, host),
             stdout=PIPE, stderr=PIPE)  ## if you don't want it to print it out
    exit_code = ping.wait()

    if exit_code != 0:
        print(host, "Host offline.")
        return False
    else:
        print(host, "Host online.")
        return True

#Continue ping until we see 5 failures.
while(True):
    if(pinger(1, 2000, host)):
        failure = 0
    else:
      failure = failure + 1
      print("add 1 to failure" , failure)
    if(failure > 5):
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
