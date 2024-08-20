import network
import urequests
import time
import esp32
import gc

SSID = 'YourSSID'
PASSWORD = 'YourPassword'

url = "http://localhost/"

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to network...')
        time.sleep(1)
    
    print('Connected. Network config:', wlan.ifconfig())

def get_cpu_ram_usage():
  
    cpu_usage = esp32.raw_temperature()
    ram_usage = gc.mem_free()
    
    return cpu_usage, ram_usage

def send_data(cpu, ram):
  
    full_url = f"{url}?cpu={cpu}&ram={ram}"
  
    try:
        response = urequests.get(full_url)
        print('Data sent:', response.text)
        response.close()
    except Exception as e:
        print('Failed to send data:', e)

if __name__ == '__main__':
    connect_to_wifi(SSID, PASSWORD)

    while True:
        cpu, ram = get_cpu_ram_usage()
        print(f"CPU Usage: {cpu}, RAM Usage: {ram}")
        send_data(cpu, ram)
        time.sleep(10)
