import serial
import time
ser = serial.Serial(
    port='COM12',\
    baudrate=5800,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
try:
    if ser.is_open:
        # Do something with the serial port
        # ...
        print("Serial port is open")
        # Close the port when finished
        # count = 0
        # while count < 10:
        print("Writing data")
        bytesWritten = ser.write(b'\0x01\0x03\0x00\0x00\0x00\0x07\0x04\0x08')
        print(bytesWritten)
        print("Data written")
        print("Reading data")
        line = ser.readline()
        # converte the bytes of line to string
        print(line)
        print("Data read")
        # sleep for 1 second
        time.sleep(1)
        # count += 1
        
        
        ser.close()
        print("Serial port is closed")

        print("Reopening serial port")
        # ser.open()
        if ser.is_open:
            print("Serial port is open")
        else:
            print("Failed to open serial port.")

    else:
        print("Failed to open serial port.")
finally:
    ser.close()  # Ensure the serial port is closed

