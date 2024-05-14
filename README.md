# How to use
## RPI Pico Setup
- Connect RPI Pico with micro usb cable (that supports data transfer) to your PC
- Install RPI Pico firmware
- Use Thonny IDE to upload all files in this repo to the device
- Adjust the user + password in config.py
- Check IP address of the device (when

## Home Assistant
- Add the following settings in configuration.yaml
```yaml
rest_command:
  markise_hoch:
    url: http://192.168.178.142:5000/up
    method: POST
  markise_runter:
    url: http://192.168.178.142:5000/down
    method: POST
  markise_stop:
    url: http://192.168.178.142:5000/stop
    method: POST
  markise_position:
    url: "http://192.168.178.142:5000/set?target={{position}}"
    method: POST
rest:
  - resource: "http://192.168.178.142:5000/status"
    scan_interval: 10
    sensor:
      - name: "MARKISE_POSITION"
        value_template: "{{ value_json['state']['percent'] | round }}"
```
