import socketserver
from instrument_simulator import DemoActualInstrument, InvalidCommand

state_instruments = {}  # key: ip address of user


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        client_ip = self.client_address[0]
        print("{} wrote: {}".format(self.client_address[0], self.data))
        if client_ip not in state_instruments:
            state_instruments[client_ip] = DemoActualInstrument()
        actual_instrument = state_instruments[client_ip]
        try:
            command_return = actual_instrument.parse_command(self.data.decode('ascii'))
            return_value = "OK;;{}".format(command_return)
        except InvalidCommand as err:
            return_value = "{};;".format(err)
        if return_value is not None:
            print('  returning {}'.format(str(return_value)))
            # just send back the same data, but upper-cased
            self.request.sendall(str(return_value).encode('ascii'))


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 6501

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
