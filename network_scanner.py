import socket
import netifaces
import subprocess
'''
Determine your own IP address
Determine your own netmask
Determine the network range
Scan all the addresses (except the lowest, which is your network address and the highest, which is your broadcast address).
Use your DNSs reverse lookup to determine the hostname for IP addresses which respond to your scan.
'''
#determine local machine ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]

print("My local ip address is: "+local_ip+" and host name is: "+ socket.gethostname())

s.close()

#determine netmask
gateway = netifaces.gateways()

#gateway for the network in which device is present
default_gateway = gateway['default'][netifaces.AF_INET][0]
print("default gateways is: "+str(default_gateway ))

#obtaining all the network interfaces
interfaces = netifaces.interfaces()

for interface in interfaces:
	print("Scanning network: "+ str(interface))
	addrs = netifaces.ifaddresses(str(interface))
	try:
		print(addrs[netifaces.AF_INET])
	except KeyError:
		print("No address assigned for interface : "+interface)
		
addrs = default_gateway.split('.')
#print("last device number of subnetwork : {}" + str(int(addrs[3])+1))
host_prefix = addrs[0]+"."+addrs[1]+"."+addrs[2]+"."
for host in range(int(addrs[3]), 255):
	ip_addr = host_prefix+str(host)
	ping = subprocess.Popen(['ping', '-c', '1', '-w', '1', ip_addr],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = ping.communicate()
	if ping.returncode == 0:
		print(ip_addr + " is available ")
	else:
		print(ip_addr + " is not available")
	'''print(error)'''