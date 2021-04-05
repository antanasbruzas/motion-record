import sys
import gpiod
import time
import liblo

with gpiod.Chip('gpiochip0') as chip:
    # TXD1 (GPIO14)
    line = chip.get_line(14)
    line.request(consumer='motion-record', type=gpiod.LINE_REQ_DIR_IN)
    lastval = 0
    try:
        while True:
            val = line.get_value()
            # Send every 30 minutes
            if (lastval != val):
                # send all messages to port 8000 on the remote machine
                try: 
                    if (val):
                        target = liblo.Address('osc.udp://192.168.11.81:8000')
                        # send message "/record" with int argument
                        liblo.send(target, "/record", 1)
                        # send message "/play" with int argument 
                        liblo.send(target, "/play", 1)
                        print("play")
                    else:
                        # send message "/stop" without arguments
                        liblo.send(target, "/stop")
                        print("stop")
                except liblo.AddressError as err:
                    print(err)
            lastval = val
            time.sleep(0.1)
    except KeyboardInterrupt:
        sys.exit(130)
