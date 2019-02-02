import socket
import netifaces
import subprocess
import time
import threading
import re
import requests

'''
Determine your own IP address
Determine your own netmask
Determine the network range
Scan all the addresses (except the lowest, which is your network address and the highest, which is your broadcast address).
Use your DNSs reverse lookup to determine the hostname for IP addresses which respond to your scan.
get mac addresses of available devices in network
get vendor name using mac address identified
'''

available_ips = []  # declaring available ips list
macs = {}  # declaring mac addresses map


# function to get local machine mac addr
def get_local_machine_mac_addr(local_ip):
    p = subprocess.Popen(["ip", "link"], stdout=subprocess.PIPE)
    data = p.communicate()[0]
    wlp2s0 = data.decode("utf-8").split("\n")[3]
    print(wlp2s0)
    macs[local_ip] = wlp2s0.strip().split(" ")[1]



# function to add mac address to macs map with key as ip address
def add_mac_addr(ip_addr):
    if ip_addr != local_ip:
        pid = subprocess.Popen(["arp", "-n", ip_addr], stdout=subprocess.PIPE)
        data = pid.communicate()[0]

        # get mac address information from ipaddress using arp -n command on linux
        mac_addr = re.sub('\s+', ',', data.decode("utf-8").split("\n")[1])
        macs[mac_addr.split(",")[0]] = mac_addr.split(",")[2]
        print(re.sub('\s+', ',', data.decode("utf-8").split("\n")[1]))


# function to check if an ip is live using ping function in unix
def check_ip_is_assigned(start, end, local_ip):

    for host in range(int(start), int(end)):
        ip_addr = host_prefix + str(host)
        if ip_addr != local_ip:
            # Ping -c for count of total number of packets to be sent
            #       -w for total number of milliseconds to be waiting
            ping = subprocess.Popen(['ping', '-c', '1', '-w', '1', '-i', '0.2', ip_addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = ping.communicate()
            if ping.returncode == 0:
                # print(ip_addr + " is available ")
                available_ips.append(ip_addr)
                add_mac_addr(ip_addr)


# function to check if an ip is assigned using socket
def check_ip_is_live(start, end, local_ip):

    for host in range(int(start), int(end)):
        ip_addr = host_prefix + str(host)
        if ip_addr != local_ip:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            try:
                result = socket_obj.connect_ex((ip_addr, 445))  # if connection successful socket connect returns 111
                if result == 111:
                    available_ips.append(ip_addr)
                    pid = subprocess.Popen(["arp", "-n", ip_addr], stdout=subprocess.PIPE)
                    data = pid.communicate()[0]
                    print(data.decode("utf-8"))
            except:
                pass
            finally:
                socket_obj.close()


# function to get vendor name from mac address
def get_oui_from_mac_addr(mac_addr):
    MAC_URL = 'http://macvendors.co/api/%s'
    r = requests.get(MAC_URL % mac_addr)
    return r.json()['result']['company']


# noting start time
start_time = time.time()

# determine local machine ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print("SOCK Details : "+ str(s.getsockname()))
local_ip = s.getsockname()[0]

print("My local ip address is: " + local_ip + " and host name is: " + socket.gethostname())
available_ips.append(local_ip)
# macs[local_ip] = "local host"
get_local_machine_mac_addr(local_ip)
s.close()

# determine netmaskavailable_ips
gateway = netifaces.gateways()

# gateway for the network in which device is present
default_gateway = gateway['default'][netifaces.AF_INET][0]
print("default gateways is: " + str(default_gateway))

# obtaining all the network interfaces like eth, wlan
interfaces = netifaces.interfaces()

for interface in interfaces:
    print("Scanning network: " + str(interface)+"\n")
    addrs = netifaces.ifaddresses(str(interface))
    try:
        print(addrs[netifaces.AF_INET])
    except KeyError:
        print("No address assigned for interface : " + interface)

addrs = default_gateway.split('.')
# print("last device number of subnetwork : {}" + str(int(addrs[3])+1))
host_prefix = addrs[0] + "." + addrs[1] + "." + addrs[2] + "."

start_addr = 1
end_addr = 26
threads = []

print("\nPlease wait while I am scanning network ...\n")

for i in range (0,10):  # making number of threads to 10 to ping asynchronously

    # making sure ip address scanning wont exceed 255
    if end_addr < 255:

        # creating multiple threads to complete the scan quickly
        t = threading.Thread(target=check_ip_is_assigned, args=(start_addr, end_addr, local_ip,))
        start_addr = start_addr + 51
        end_addr = end_addr + 52
        t.start()
        threads.append(t)

# joining all the threads
for t in threads:
    t.join()

# showing available IP's
print("LIVE IP\'S AVAILABLE ARE: ")
for ip in available_ips:

    # getfqdn will convert ipaddress into hostname
    print(ip+" - "+socket.getfqdn(ip) + " - mac addr : " + macs[ip] + " - Vendor : "+get_oui_from_mac_addr(macs[ip]))

# time taken for completing whole task
duration = time.time() - start_time

# calculating total time taken for the execution
print(f"Total time taken is {duration} seconds")
