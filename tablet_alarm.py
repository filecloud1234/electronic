import network
import socket
from machine import Pin
import time

# Set up a pin to be turned on/off
pin = Pin(2, Pin.OUT)  # Change to the desired GPIO pin
pin.off()

# Global variables for alarm time and color
alarm_time = None
alarm_color = None

def create_ap():
    """
    Create a Wi-Fi Access Point with SSID 'ESP32-AP' and password '12345678'.
    """
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32-AP', password='12345678')  # Set the AP name and password

    while not ap.active():
        pass
    
    print('Network Config:', ap.ifconfig())

def web_page():
    """
    Serve the web page with a form to set the timer and color.
    """
    html = """<!DOCTYPE html>
    <html>
    <head>
    <title>ESP32 Timer</title>
    </head>
    <body>
    <h2>Set Timer and Color</h2>
    <form action="/" method="GET">
      <label for="time">Set Alarm Time (in seconds):</label><br><br>
      <input type="number" id="time" name="time"><br><br>
      <label for="color">Choose Color:</label><br><br>
      <input type="color" id="color" name="color"><br><br>
      <input type="submit" value="Set Timer">
    </form>
    </body>
    </html>"""
    return html

def start_web_server():
    """
    Start the web server to handle requests and serve the web page.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print("Web server started, listening on port 80.")

    while True:
        conn, addr = s.accept()
        print('Connection from:', addr)
        
        request = conn.recv(1024).decode()
        print('Request:', request)
        
        if 'GET /?' in request:
            params = request.split(' ')[1].split('?')[1]
            params = params.split('&')
            global alarm_time, alarm_color
            alarm_time = int(params[0].split('=')[1])
            alarm_color = params[1].split('=')[1]
            print(f"Timer set to: {alarm_time} seconds and color: {alarm_color}")
        
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

def run_timer():
    """
    Monitor the timer and activate the pin when the time is reached.
    """
    start_time = time.time()
    global alarm_time
    
    while True:
        current_time = time.time()
        if alarm_time is not None and (current_time - start_time) >= alarm_time:
            pin.on()  # Turn on the pin
            print(f"Alarm triggered! Color: #{alarm_color}")
            alarm_time = None  # Reset the alarm
            break

# Main Program
if __name__ == '__main__':
    create_ap()  # Create the Access Point
    start_web_server()  # Start the web server

    # Continuously run the timer check in a separate loop
    while True:
        run_timer()
