import serial.tools.list_ports


def get_ports():
    port_number = None
    ports = list(serial.tools.list_ports.comports())

    for port in ports:
        if port.manufacturer.startswith('STM'):
            port_number = port.device

    return port_number


def receive_data(iot_device):
    try:
        value = iot_device.readline()
        print(value)
    except serial.SerialException as e:
        print(e)


if __name__ == "__main__":
    port_number = get_ports()
    iot_device = serial.Serial(port=port_number, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=1)

    while True:
        receive_data(iot_device)
