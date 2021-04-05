import sys
import gpiod
import time
import liblo

with gpiod.Chip('gpiochip0') as chip:
    # TXD1 (GPIO14)
    line = chip.get_line(14)
    line.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_IN)
    recording = False
    try:
        if (len(sys.argv) > 1):
            # Send all messages to arg specified target
            target = liblo.Address(sys.argv[1]) 
        else:
            # Send all messages to port 8000 on localhost
            target = liblo.Address(8000)
        while True:
            val = line.get_value()
            if (val):
                # Could be expensive
                motionTimestamp = time.time()
                if (not recording):
                    # Send message "/record" with int argument
                    liblo.send(target, "/record", 1)
                    # Send message "/play" with int argument 
                    liblo.send(target, "/play", 1)
                    recording = True
                    print("play")
            else:
                # Send only if no motion was detected for 30 minutes
                if (recording and time.time() - motionTimestamp > 1800):
                    # Send message "/stop" without arguments
                    liblo.send(target, "/stop")
                    recording = False;
                    print("stop")
            time.sleep(0.1)
    except liblo.AddressError as err:
        print(err)
    except KeyboardInterrupt:
        sys.exit(130)
