import serial
import time

class Sensor:
    def __init__(self, port='COM12', baudrate=4800):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=5)

    @staticmethod
    def twos_complement(hexstr, bits):
        value = int(hexstr, 16)
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value

    def send_command(self, command):
        if not self.ser.is_open:
            raise serial.SerialException("Serial port is not open")
        
        bytesWritten = self.ser.write(command)
        print(f"Bytes written: {bytesWritten}")
        print(f"Data sent (hex): {command.hex()}")
        time.sleep(0.1)  # Short delay after sending

    def read_response(self, timeout=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ser.in_waiting:
                response = self.ser.read(self.ser.in_waiting)
                print(f"Received: {response.hex()}")
                return response
            time.sleep(0.1)
        raise TimeoutError("No data received within the specified timeout")

    def process_data(self, data):
        num_data_bytes = data[2]
        data_bytes = data[3:3+num_data_bytes]

        result = []
        for i in range(0, len(data_bytes), 2):
            hex_value = data_bytes[i:i+2].hex()
            decimal_value = self.twos_complement(hex_value, 16)
            final = decimal_value / 10
            result.append(final)

        return result

    def get_all_data(self):
        try:
            command = b'\x01\x03\x00\x00\x00\x07\x04\x08'
            self.send_command(command)
            response = self.read_response()
            result = self.process_data(response)

            if len(result) != 7:
                raise ValueError(f"Expected 4 values, got {len(result)}")

            return {
                "humidity": result[0],
                "temperature": result[1],
                "conductivity": result[2],
                "ph": result[3],
                "nitrogen": result[4],
                "phosphorus": result[5],
                "potassium": result[6]
            }

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def close(self):
        if self.ser.is_open:
            self.ser.close()

    def __del__(self):
        self.close()

# Usage example:
if __name__ == "__main__":
    sensor = Sensor()  # Create sensor object
    try:
        # while no key is pressed
        while True:
            data = sensor.get_all_data()
            if data:
                print("Sensor readings not npk:", data)
            time.sleep(1) # can change to 3 hours for easy value reading
            if input("0 to exit, any other key to continue: ") == "0":
                break
    finally:
        sensor.close() 
