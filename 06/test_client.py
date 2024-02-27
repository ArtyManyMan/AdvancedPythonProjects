import unittest
from client import TCPClient
from unittest import mock
from unittest.mock import patch
import threading


class TestTCPClient(unittest.TestCase):

    @patch('client.TCPClient.reciver')
    @patch('client.socket')
    @patch('client.threading')
    def test_init(self, mock_threading, mock_socket, mock_reciver):

        ip = 'localhost'
        port = 12345
        th = 15
        file_name = 'file_name'

        cli = TCPClient(ip, port, th, file_name)

        self.assertEqual(th, cli.quantity_th)
        self.assertEqual(cli.filename, file_name)
        self.assertEqual(cli.sock, mock_socket.socket.return_value)
        self.assertTrue(mock_socket.socket.return_value.connect.called_once())
        self.assertIsNone(mock_socket.socket.return_value.connect.assert_has_calls([mock.call((ip, port))]))
        self.assertEqual(cli.lock, mock_threading.Lock.return_value)
        self.assertTrue(cli.reciver.called_once())

    @patch('client.socket')
    @patch('client.threading')
    def test_reciver(self, mock_threading, mock_socket):

        mock_socket.socket.return_value.recv.return_value = None

        ip = 'localhost'
        port = 12345
        th = 15
        file_name = 'file_name'

        cli = TCPClient(ip, port, th, file_name)

        self.assertTrue(mock_socket.socket.return_value.close.called_once())

        lst_args = [b'Test text'] * 5 + [None]
        mock_socket.socket.return_value.recv.side_effect = lst_args

        with patch('builtins.print') as mock_print:
            TCPClient(ip, port, th, file_name)

        self.assertEqual(len(lst_args) + 1, cli.sock.recv.call_count)

        for i in mock_print.call_args_list:
            self.assertEqual(mock.call('Test text'), i)

        self.assertTrue(mock_socket.socket.return_value.close.called_once())

    @patch('client.TCPClient.reciver')
    @patch('client.socket')
    @patch('client.threading')
    def test_file_reader(self, mock_threading, mock_socket, mock_reciver):
        ip = 'localhost'
        port = 12345
        th = 15
        file_name = 'url_lib.txt'

        cli = TCPClient(ip, port, th, file_name)
        cli.file_reader()

        with open(file_name) as file:
            for i in file:
                self.assertEqual(i, cli.que.get())

        for i in range(th):
            self.assertIsNone(cli.que.get())

        self.assertTrue(cli.que.empty())

    @patch('client.threading')
    @patch('client.TCPClient.extractor')
    @patch('client.TCPClient.file_reader')
    @patch('client.TCPClient.reciver')
    @patch('client.socket')
    def test_worker(self, mock_socket, mock_reciver, mock_file_reader, mock_extractor, mock_threading):
        ip = 'localhost'
        port = 12345
        th = 15
        file_name = 'url_lib.txt'

        cli = TCPClient(ip, port, th, file_name)

        def func():
            cli.worker()

        thread = threading.Thread(target=func)
        thread.start()
        thread.join(timeout=5)

        self.assertEqual(th, mock_extractor.call_count)

        th = 5
        file_name = 'url_lib.txt'

        cli = TCPClient(ip, port, th, file_name)

        def func():
            cli.worker()

        thread = threading.Thread(target=func)
        thread.start()
        thread.join(timeout=5)

        self.assertEqual(20, mock_extractor.call_count)

        th = 1
        file_name = 'url_lib.txt'

        cli = TCPClient(ip, port, th, file_name)

        def func():
            cli.worker()

        thread = threading.Thread(target=func)
        thread.start()
        thread.join(timeout=5)

        self.assertEqual(21, mock_extractor.call_count)

if __name__ == '__main__':
    unittest.main()