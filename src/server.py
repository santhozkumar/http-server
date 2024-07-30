import socket
import threading



class Server:
    def setup(self, config):
        self.config = config
        self.socket = None




    def run(self):
        listen_port = self.config['port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.config['address'], listen_port))
        self.socket.listen(self.config.get('backlog', 3))
        print('binding done')
        return self.socket

    def shutdown(self):
        if self.socket:
            self.socket.close()

