import network
import time

SSID = '<MyWLAN>'
PASSWORD = '<MyPassword>'
IP = "0.0.0.0"

def get_ip():
    return IP

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        IP = status[0]
        print( 'ip = ' + IP + ' port = 5000' )
        
