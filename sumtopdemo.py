import socket
from lightlab.equipment.lab_instruments import VISAInstrumentDriver
from lightlab.equipment.visa_bases.driver_base import TCPSocketConnection


class TCPInstrumentDriver(VISAInstrumentDriver):
    '''Instrument-driver not based on VISA.
    This code was written for the demo but should be included in the main codebase.
    '''

    def reinstantiate_session(self, address, tempSess):
        if address is not None:
            # should be something like ['TCPIP0', 'xxx.xxx.xxx.xxx', '6501', 'SOCKET']
            address_array = address.split("::")
            self._tcpsocket = TCPSocketConnection(ip_address=address_array[1],
                                                  port=int(address_array[2]),
                                                  timeout=5,
                                                  termination='\n')

    def open(self):
        if self.address is None:
            raise RuntimeError("Attempting to open connection to unknown address.")
        try:
            self._tcpsocket.connect()
        except socket.error:
            self._tcpsocket.disconnect()
            raise

    def close(self):
        self._tcpsocket.disconnect()

    def query(self, query_str):
        with self._tcpsocket.connected():
            self._tcpsocket.send(query_str)
            received_message = self._tcpsocket.recv()
            try:
                status, message = received_message.split(';;', maxsplit=1)
            except ValueError:
                raise RuntimeError('An unexpected error occured.')
            if status == 'OK':
                if message == '':
                    return None
                else:
                    return message
            else:
                raise RuntimeError('Bad command. {}'.format(status))

    def write(self, write_str):
        return self.query(write_str)
