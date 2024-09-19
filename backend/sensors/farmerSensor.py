import serial
import serial.tools.list_ports
import time

# List available ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

# Try to find the CH340 device
ch340_port = next((p.device for p in ports if 'CH340' in p.description), None)

if ch340_port:
    print(f"CH340 device found on port: {ch340_port}")
else:
    print("CH340 device not found. Please check the connection and try again.")
    exit(1)

# Configure the serial port
ser = serial.Serial(
    port=ch340_port,  # Use the detected CH340 port
    baudrate=4800,    # Baud rate (you may need to adjust this)
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

try:
    print("attempting to read from serial port")
    while True:
        # Read data from the serial port
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {data}")
        # print("Waiting for data...")
        time.sleep(0.1)  # Small delay to prevent busy-waiting

except KeyboardInterrupt:
    print("Exiting program")
finally:
    ser.close() 
