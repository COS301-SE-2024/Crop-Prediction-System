import serial
import time
ser = serial.Serial(
    port='COM12',
    baudrate=4800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE, 
    bytesize=serial.EIGHTBIT)
try:
    if ser.is_open:
        # Do something with the serial port
        # ...
        print("Serial port is open")
        # Close the port when finished
        # count = 0
        # while count < 10:
        print("Writing data")
        data_to_send = b'\x01\x04\x00\x00\x00\x04\x44\x09' # 01 04 00 00 00 04 44 09
        bytesWritten = ser.write(data_to_send)
        print(f"Bytes written: {bytesWritten}")
        print(f"Data sent (hex): {data_to_send.hex()}")
        # sleep for 0.1 second 
        time.sleep(0.1)
        print(bytesWritten)
        print("Data written")
        print("Reading data")
        start_time = time.time()
        while time.time() - start_time < 5:  # Wait up to 2 seconds for data
            if ser.in_waiting:
                line = ser.read(ser.in_waiting)
                print(f"Received: {line.hex()}")
                break
            time.sleep(0.1)
        else:
            print("No data received")
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
