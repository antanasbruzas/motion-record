import sys
import gpiod
import time
import liblo

with gpiod.Chip('gpiochip0') as chip:
    if (len(sys.argv) > 1):
        # Use arg specified line
        line = chip.get_line(int(sys.argv[1]))
    else:
        # TXD1 (GPIO14)
        line = chip.get_line(14)
    line.request(consumer=sys.argv[0], type=gpiod.LINE_REQ_DIR_IN)
    recording = False
    try:
        if (len(sys.argv) > 2):
            # Send all messages to arg specified target
            target = liblo.Address(sys.argv[2]) 
        else:
            # Send all messages to port 8000 on localhost
            target = liblo.Address(8000)
        while True:
            val = line.get_value()
            if (val):
                # Could be expensive
                motionTimestamp = time.time()
                if (not recording):
                    # Send message "/record"
                    liblo.send(target, "/record")
                    # Send message "/play" with int argument 
                    liblo.send(target, "/play", 1)
                    recording = True
                    print("play")
            else:
                # Send only if no motion was detected for 30 minutes
                if (recording and time.time() - motionTimestamp > 1800):
                    # Send message "/play" with int argument
                    liblo.send(target, "/play", 0)
                    # Send messages to save the project
                    time.sleep(1)
                    liblo.send(target, "/project/save")
                    recording = False;
                    print("stop")
            time.sleep(0.1)
    except liblo.AddressError as err:
        print(err)
    except KeyboardInterrupt:
        sys.exit(130)

