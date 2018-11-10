import socket
import netifaces
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
default_gateway = gateway['default'][netifaces.AF_INET][0]
print("default gateways is: "+str(default_gateway ))

interfaces = netifaces.interfaces()

for interface in interfaces:
	print("Scanning network: "+ str(interface))
	addrs = netifaces.ifaddresses(str(interface))
	try:
		print(addrs[netifaces.AF_INET])
	except KeyError:
		print("No address assigned for interface : "+interface)