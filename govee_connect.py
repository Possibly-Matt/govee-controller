from gattlib import GATTRequester

class BluetoothLED:
    """ Bluetooth client for Govee's RGB LED H6001. """
     def __init__(self, address):
        self.address = address
        self.requester = GATTRequester(self.address, False)
        self.connect()

    def connect(self):
        print("Connecting...")

        self.requester.connect(True)
        print("OK!")

    def keepAlive(self)

    def send_data(self, command, payload):
        self.requester.write_by_handle(0x2e, str(bytearray([2])))

    def set_state(self, powerstate):
        if (powerstate):
            value = 12
        else:
            value = 11

        send_data()