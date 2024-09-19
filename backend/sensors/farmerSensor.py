import serial
import time

# Function to convert a hex string to a list of decimal pairs
def twos_complement(hexstr,bits):
    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

# Open the serial port
ser = serial.Serial(
    port='COM12',
    baudrate=4800)

try:
    if ser.is_open:
        print("Serial port is open")
        print("Writing data")
        data_to_send = b'\x01\x03\x00\x00\x00\x04\x44\x09' # 01 03 00 00 00 04 44 09
        bytesWritten = ser.write(data_to_send)
        print(f"Bytes written: {bytesWritten}")
        print(f"Data sent (hex): {data_to_send.hex()}")
        # sleep for 0.1 second 
        time.sleep(0.1)
        print(bytesWritten)
        print("Data written")
        print("Reading data")
        start_time = time.time()
        line = ""
        while time.time() - start_time < 5:  # Wait up to 5 seconds for data
            if ser.in_waiting:
                line = ser.read(ser.in_waiting)
                print(f"Received: {line.strip()}")
                break
            time.sleep(0.1)
        else:
            print("No data received")
        print("Data read")
        # sleep for 1 second
        time.sleep(1)
        # Convert the hex string to decimal pairs
        
        num_data_bytes = line[2]
        dataBytes = line[3:3+num_data_bytes]

        result = []
        for i in range(0, len(dataBytes), 2):
            hex_value = dataBytes[i:i+2].hex()
            decimal_value = twos_complement(hex_value, 16)
            final = decimal_value / 10
            result.append(final)

        print("Data pairs:", result)
        moisture = result[0]
        temperature = result[1]
        conductivity = result[2]
        ph = result[3]
        
    else:
        print("Failed to open serial port.")
finally:
    ser.close()  # Ensure the serial port is closed
