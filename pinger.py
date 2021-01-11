import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from netmiko import Netmiko
from getpass import getpass

host=input("enter target ping IP: ")
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

while(True):
    if(not ping(host)):
      failure = failure + 1
    if(failure > 2):
      break

print('exited loop, execute switch command')

device = {
    "device_type": "cisco_xe",
    "ip": switch,
    "username": username,
    "password": password,
}

connect = Netmiko(**device)
output = connect.send_command("show ver")
connect.disconnect

print(output)
