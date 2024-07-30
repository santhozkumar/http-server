import queue
import threading

from typing import Type
from time import sleep

DUMMY_RESPONSE = '''HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Type: text/html
Content-Length: 50
Connection: Closed
<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>'''



class Worker:
    is_stopped:bool= False
    def setup(self, config):
        self.config = config
        self.queue = queue.Queue(maxsize=10)
        self.kill_pill = threading.Event()
        threads = [RequestThreadProcessor(name=f'RequestThreadProcessor{i}', queue=self.queue, kill_pill=self.kill_pill) for i in range(self.config.get('concurrency', 1))]
        for thread in threads:
            thread.start()

    def run(self, listener):
        while not self.is_stopped:
            print('worker called')
            socket, _ = listener.accept()
            self.submit(socket)

    def submit(self, sock):
        try:
            self.queue.put(sock, timeout=self.config.get('timeout', 5))
        except queue.Full:
            print("queue full")
            pass
        
    def shutdown(self):
        self.is_stopped=True
        self.kill_pill.set()





class RequestThreadProcessor(threading.Thread):
    def __init__(self, group=None, target=None, name=None,queue=None, kill_pill=None, args=(), kwargs=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self.queue: Type[queue.Queue] = queue
        self.kill_pill = kill_pill


    def run(self):
        while not self.kill_pill.is_set():
            try:
                sock = self.queue.get(block=True, timeout=1)
                self.process(sock)
            except queue.Empty:
                continue
        

        
    def process(self, sock):

        chunk = sock.recv(1000)
        print(chunk)
        sleep(1)

        sock.send(str.encode(DUMMY_RESPONSE))
        sock.close()
