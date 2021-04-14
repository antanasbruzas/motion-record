# motion-record
Trigger DAW recording with OSC when detected by PIR sensor

## Dependencies
`sudo apt install python3-libgpiod python3-liblo`

## Run
`python3 motion-record.py 14 'osc.udp://192.168.8.102:8000'`
