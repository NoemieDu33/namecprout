import serial,time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        ser.write(b"Straight\n")
        time.sleep(1)
        ser.close()
        exit()