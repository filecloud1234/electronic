import wifi
import socketpool
import time
import ipaddress
print("Creating Access Point")

ipv4 = ipaddress.IPv4Address("192.168.10.2")
netmask = ipaddress.IPv4Address("255.255.255.0")
gateway = ipaddress.IPv4Address("192.168.1.1")
wifi.radio.stop_ap()
wifi.radio.start_ap(ssid="Cake", password="12345678",
                    max_connections=20)
wifi.radio.set_ipv4_address_ap(ipv4=ipv4, netmask=netmask, gateway=gateway)

#wifi.radio.stop_dhcp_ap()
#wifi.radio.start_dhcp_ap()

status = wifi.radio.ap_active
print("Access Point Created: Status " + str(status))
print("IP Adress Is:", wifi.radio.ipv4_gateway_ap)
pool = socketpool.SocketPool(wifi.radio)
print("Pool Created")

socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
socket.settimeout(100)
socket.connect(("0.0.0.0", 5000))
print("Connected")

while True:
    socket.send(b'hello")
    time.sleep(1)

