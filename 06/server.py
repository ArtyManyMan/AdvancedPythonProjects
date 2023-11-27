import socket
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
import select
import selectors
import requests
from collections import Counter
import json
import re
from bs4 import BeautifulSoup


class TCPServer:

    def __init__(self, n_workers, k_words):
        self.n_workers = n_workers
        self.k_words = k_words
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('localhost', 12345))
        self.selector = selectors.DefaultSelector()
        self.lock = threading.Lock()
        self.count = 0
        self.que = Queue()

        self.stop_flag = False

        self.thread_workers = threading.Thread(target=self.workers)
        self.thread_workers.start()

        self.master()

    def master(self):
        self.sock.listen(0)
        self.sock.setblocking(False)
        inputs = [self.sock]
        while not self.stop_flag:
            try:
                readable, _, _ = select.select(inputs, [], [])
                for s in readable:
                    if self.stop_flag:
                        break
                    if s is self.sock:
                        client_socket, addr = self.sock.accept()
                        print('New connection from', addr)
                        client_socket.setblocking(False)
                        inputs.append(client_socket)
                    else:
                        data = s.recv(1024)
                        if not data:
                            print('Connection closed')
                            inputs.remove(s)
                            s.close()
                        else:
                            for i in data.decode().split():
                                self.que.put((i, client_socket), timeout=1)

            except KeyboardInterrupt:
                client_socket.close()
                print("KeyboardInterrupt detected")
                self.stop_flag = True
                break
        self.sock.close()
        print("Exited master loop")

    def workers(self):
        print("Starting workers")
        with ThreadPoolExecutor(max_workers=self.n_workers, thread_name_prefix='Thread') as executor:
            futures = []
            for _ in range(self.n_workers):
                futures.append(executor.submit(self.url_parser))

            for future in futures:
                future.result()

        executor.shutdown(wait=True)
        print('Workers shutdown')

    def url_parser(self):
        while not self.stop_flag:
            try:
                url, client_socket = self.que.get(timeout=1)
                try:
                    response = requests.get(url, timeout=5)
                    if response.encoding is None:
                        with self.lock:
                            print(f"Кодировка не определена для сайта {url}. Пропуск обработки.")
                            continue

                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')

                        text = soup.get_text(separator=' ', strip=True)
                        text = re.sub(r'\s+', ' ', text)

                        self.words_counter(text, url, client_socket)

                    else:
                        with self.lock:
                            print(f"Ошибка {response.status_code} при загрузке страницы {url}")
                except requests.exceptions.ContentDecodingError as e:
                    with self.lock:
                        print(f"Произошла ошибка декодирования содержимого для сайта {url}. Пропуск обработки.")
                except requests.exceptions.RequestException as e:
                    with self.lock:
                        print(f"Произошла ошибка при запросе URL {url}: {e}")
            except Empty:
                continue

    def words_counter(self, text, url, client_socket):
        res = {}
        sorted_words = Counter(text.split()).most_common()
        for i in range(self.k_words):
            if len(sorted_words) > i:
                res[sorted_words[i][0]] = sorted_words[i][1]
        with self.lock:
            self.count += 1
            print(f"Обработано {self.count} URL всеми воркерами.")
            msg = json.dumps(res, ensure_ascii=False)
            self.send_msg(client_socket, msg)

    def send_msg(self, client_socket, msg):
        client_socket.send(msg.encode())


if __name__ == '__main__':
    server_module = argparse.ArgumentParser(description='TCP Server with parameters')
    server_module.add_argument('-w', type=int, help='Number of workers')
    server_module.add_argument('-k', type=int, help='Top k of most popular words')

    args = server_module.parse_args()

    serv = TCPServer(args.w, args.k)
