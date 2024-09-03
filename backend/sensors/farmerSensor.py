from pymodbus.client import ModbusTcpClient

# create client object
deviceLan = ""
client = ModbusTcpClient(deviceLan)
client.connect()

# set information in device
client.write_coil(1, True, slave=1)

#  get information from device
result = client.read_coils(2, 3, slave=1)

print(result.bits[0]) #use the info

# close connection
client.close()