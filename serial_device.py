import serial.tools.list_ports


def get_ports():
    port_number = None
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        # Test1
        print(port.manufacturer)

        if port.manufacturer.startswith('STM'):
            port_number = port.device

        # Test2
        # print(port_number)

    return port_number

print(get_ports())