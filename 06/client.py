import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import argparse


class TCPClient:

    def __init__(self, ip, port, quantity_th, filename):
        self.quantity_th = quantity_th
        self.filename = filename
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.lock = threading.Lock()
        self.que = Queue()
        threading.Thread(target=self.file_reader).start()
        threading.Thread(target=self.worker).start()
        self.reciver()

    def sender_msg(self, msg):
        with self.lock:
            self.sock.send((msg + '\n').encode())

    def file_reader(self):
        with open(self.filename, 'r') as file:
            for i in file:
                self.que.put(i)
            for j in range(self.quantity_th):
                self.que.put(None)
    def extractor(self):
        while True:
            msg = self.que.get()
            if msg is None:
                break
            self.sender_msg(msg)

    def worker(self):

        with ThreadPoolExecutor(max_workers=self.quantity_th) as executor:
            futures = []
            for i in range(self.quantity_th):
                futures.append(executor.submit(self.extractor))
            for j in futures:
                j.result()
        executor.shutdown(wait=True)
    def reciver(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(data.decode())
        self.sock.close()


if __name__ == '__main__':
    client_module = argparse.ArgumentParser(description='TCP Client with parameters')
    client_module.add_argument('M', type=int, help='Number of worker threads')
    client_module.add_argument('filename', type=str, help='File name to read from')

    args = client_module.parse_args()

    cli = TCPClient('localhost', 12345, args.M, args.filename)
