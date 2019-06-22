import socket
import netifaces
import subprocess
import time
import multiprocessing

'''
Determine your own IP address
Determine your own netmask
Determine the network range
Scan all the addresses (except the lowest, which is your network address and the highest, which is your broadcast address).
Use your DNSs reverse lookup to determine the hostname for IP addresses which respond to your scan.
'''

available_ips = []


def check_ip_is_assigned(start, end):
    for host in range(int(start), int(end)):
        ip_addr = host_prefix + str(host)
        ping = subprocess.Popen(['ping', '-c', '1', '-w', '1', ip_addr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = ping.communicate()
        if ping.returncode == 0:
            print(ip_addr + " is available ")
            available_ips.append(ip_addr)
        else:
            print(ip_addr + " is not available")


# noting start time
start_time = time.time()

# determine local machine ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]

print("My local ip address is: " + local_ip + " and host name is: " + socket.gethostname())

s.close()

# determine netmask
gateway = netifaces.gateways()

# gateway for the network in which device is present
default_gateway = gateway['default'][netifaces.AF_INET][0]
print("default gateways is: " + str(default_gateway))

# obtaining all the network interfaces
interfaces = netifaces.interfaces()

for interface in interfaces:
    print("Scanning network: " + str(interface))
    addrs = netifaces.ifaddresses(str(interface))
    try:
        print(addrs[netifaces.AF_INET])
    except KeyError:
        print("No address assigned for interface : " + interface)

addrs = default_gateway.split('.')
# print("last device number of subnetwork : {}" + str(int(addrs[3])+1))
host_prefix = addrs[0] + "." + addrs[1] + "." + addrs[2] + "."

start = 0
end = 51
threads = []

print("Please wait while we are scanning network ...")

for i in range (0,5):

    # making sure ip address scanning wont exceed 255
    if end < 256:
        t = multiprocessing.Process(target=check_ip_is_assigned, args=(start, end,))
        start = start + 51
        end = end + 52
        t.start()
        threads.append(t)

# joining all the threads
for t in threads:
    t.join()

print(str(available_ips))
duration = time.time() - start_time

# calculating total time taken for the execution
print(f"Total time taken is {duration} seconds")
