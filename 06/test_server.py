import unittest
from unittest.mock import patch, MagicMock, Mock
from unittest import mock
import server
import threading


class TestTCPServer(unittest.TestCase):

    @patch('server.argparse')
    @patch('server.TCPServer.master')
    @patch('server.selectors')
    @patch('server.socket')
    @patch('server.threading')
    def test_init(self, mock_threading, mock_socket, mock_selectors, mock_TCPServer_master, mock_argparse):

        serv = server.TCPServer(10, 3)

        self.assertEqual(serv.n_workers, 10)
        self.assertEqual(serv.k_words, 3)
        self.assertEqual(serv.sock, mock_socket.socket())
        self.assertEqual(serv.selector, mock_selectors.DefaultSelector())
        self.assertEqual(serv.lock, mock_threading.Lock())
        self.assertEqual(serv.count, 0)
        self.assertEqual(serv.thread_workers, mock_threading.Thread())

    @patch('server.argparse')
    @patch('server.selectors')
    @patch('server.socket')
    @patch('server.threading')
    def test_master_accept_and_listen(self, mock_threading, mock_socket, mock_selectors, mock_argparse):

        with self.assertRaises(TypeError):
            serv = server.TCPServer(10, 3)

        mock_socket = mock_socket.socket()
        mock_socket.listen = MagicMock()
        mock_socket.setblocking = MagicMock()

        with patch('server.select.select', return_value=([''], [], [])):
            with self.assertRaisesRegex(AttributeError, "'str' object has no attribute 'recv'"):
                serv = server.TCPServer(10, 3)

        mock_socket.listen.assert_called()
        self.assertEqual((0,), mock_socket.listen.call_args_list[0][0])
        self.assertIsNone(mock_socket.listen.assert_called_with(0))

        with patch('builtins.print') as mock_print:
            with patch('server.select.select', return_value=([mock_socket], [], [])):
                def run_server():
                    serv = server.TCPServer(10, 3)

                thread = threading.Thread(target=run_server)
                thread.start()
                thread.join(timeout=1)

        mock_socket.accept.assert_called()
        self.assertIsNone(mock_socket.accept.assert_called_with())

    @patch('server.TCPServer.url_parser')
    @patch('server.TCPServer.master')
    @patch('server.socket')
    def test_workers(self, mock_socket, mock_master, mock_url_parser):

        with patch('builtins.print') as mock_print:
            serv = server.TCPServer(10, 3)
            self.assertTrue(serv.thread_workers.is_alive())
            serv.thread_workers.join()

        expected_calls = [mock.call('Starting workers'), mock.call('Workers shutdown')]

        self.assertEqual(mock_print.call_args_list, expected_calls)
        self.assertEqual(10, mock_url_parser.call_count)
        self.assertFalse(serv.thread_workers.is_alive())

        with patch('builtins.print') as mock_print:
            serv = server.TCPServer(5, 1)
            self.assertTrue(serv.thread_workers.is_alive())
            serv.thread_workers.join()

        expected_calls = [mock.call('Starting workers'), mock.call('Workers shutdown')]

        self.assertEqual(mock_print.call_args_list, expected_calls)
        self.assertEqual(15, mock_url_parser.call_count)
        self.assertFalse(serv.thread_workers.is_alive())

        with patch('builtins.print') as mock_print:
            serv = server.TCPServer(1, 1)
            self.assertTrue(serv.thread_workers.is_alive())
            serv.thread_workers.join()

        expected_calls = [mock.call('Starting workers'), mock.call('Workers shutdown')]

        self.assertEqual(mock_print.call_args_list, expected_calls)
        self.assertEqual(16, mock_url_parser.call_count)
        self.assertFalse(serv.thread_workers.is_alive())

    @patch('server.Queue')
    @patch('server.TCPServer.master')
    @patch('server.socket')
    def test_connect_between_workers_and_url_parser(self, mock_socket, mock_master, mock_Queue):

        with patch('builtins.print') as mock_print:
            serv = server.TCPServer(1, 3)
            serv.thread_workers.join(timeout=1)
            serv.stop_flag = True

        expected_print_calls = [mock.call("Starting workers")]
        self.assertIsNone(mock_print.assert_called_once())
        self.assertEqual(mock_print.call_args, expected_print_calls[0])

        self.assertIsNone(mock_Queue.return_value.get.assert_called_with(timeout=1))

    @patch('server.requests')
    @patch('server.threading')
    @patch('server.TCPServer.workers')
    @patch('server.TCPServer.master')
    @patch('server.socket')
    def test_url_parser_wrong_status_code(self, mock_socket, mock_master, mock_workers, mock_threading, mock_requests):
        client_socket = MagicMock()
        mock_requests.get.return_value.status_code = 400
        serv = server.TCPServer(1, 3)
        serv.que.put(('http://wildberries.ru', client_socket))

        with patch('builtins.print') as mock_print:
            thread = threading.Thread(target=serv.url_parser)
            thread.start()
            thread.join(timeout=1)
            serv.stop_flag = True

        self.assertIsNone(mock_print.assert_called_once())
        expected_print_calls = [mock.call("Ошибка 400 при загрузке страницы http://wildberries.ru")]
        self.assertEqual(expected_print_calls[0], mock_print.call_args)

    @patch('server.re')
    @patch('server.BeautifulSoup')
    @patch('server.TCPServer.words_counter')
    @patch('server.requests')
    @patch('server.threading')
    @patch('server.TCPServer.workers')
    @patch('server.TCPServer.master')
    @patch('server.socket')
    def test_url_parser_status_code_200(self, mock_socket, mock_master,
                                          mock_workers, mock_threading,
                                          mock_requests, mock_words_counter,
                                          mock_Beautiful_Soap, mock_re):

        client_socket = MagicMock()


        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = 'Test text'
        mock_re.sub.return_value = 'Test text'

        serv = server.TCPServer(1, 3)
        serv.que.put(('http://wildberries.ru', client_socket))

        with patch('builtins.print') as mock_print:
            thread = threading.Thread(target=serv.url_parser)
            thread.start()
            thread.join(timeout=1)
            serv.stop_flag = True

        self.assertIsNone(mock_requests.get.assert_called_once())
        self.assertIsNone(mock_requests.get.assert_has_calls([mock.call('http://wildberries.ru', timeout=5)]))

        self.assertIsNone(mock_Beautiful_Soap.assert_called_once())
        self.assertIsNone(mock_Beautiful_Soap.assert_has_calls([mock.call('Test text', 'html.parser')]))

        expected_calls = [mock.call('Test text', 'http://wildberries.ru', client_socket)]
        self.assertIsNone(mock_words_counter.assert_called_once())
        self.assertEqual(mock_words_counter.call_args, expected_calls[0])

    @patch('server.TCPServer.words_counter')
    @patch('server.requests')
    @patch('server.threading')
    @patch('server.TCPServer.workers')
    @patch('server.TCPServer.master')
    @patch('server.socket')
    def test_url_parser_encoding_is_None(self, mock_socket, mock_master,
                                        mock_workers, mock_threading,
                                        mock_requests, mock_words_counter):

        client_socket = MagicMock()

        mock_requests.get.return_value.encoding = None

        serv = server.TCPServer(1, 3)
        serv.que.put(('http://wildberries.ru', client_socket))

        with patch('builtins.print') as mock_print:
            thread = threading.Thread(target=serv.url_parser)
            thread.start()
            thread.join(timeout=1)
            serv.stop_flag = True

        self.assertIsNone(mock_print.assert_called_once())
        self.assertIsNone(mock_print.assert_called_with(f"Кодировка не определена для сайта http://wildberries.ru. Пропуск обработки."))

    @patch('server.TCPServer.send_msg')
    @patch('server.TCPServer.url_parser')
    @patch('server.requests')
    @patch('server.threading')
    @patch('server.TCPServer.workers')
    @patch('server.TCPServer.master')
    @patch('server.socket')
    def test_words_counter(self, mock_socket, mock_master,
                           mock_workers, mock_threading,
                           mock_requests, mock_url_parser, mock_send_msg):

        text = 'А роза упала на лапу Азора, а зорро дал на лапу газону, газон газонул и уехал в закакт, за этим следил дозорных отряд.'
        url = 'anecdot.ru'
        client_socket = MagicMock()

        serv = server.TCPServer(1, 3)

        with patch('builtins.print') as mock_print:
            serv.words_counter(text, url, client_socket)
        self.assertEqual(mock.call('Обработано 1 URL всеми воркерами.'), mock_print.call_args)
        self.assertIsNone(mock_send_msg.assert_called_once())

        self.assertEqual(mock.call(client_socket, '{"на": 2, "лапу": 2, "А": 1}'), mock_send_msg.call_args)

    @patch('server.TCPServer.send_msg')
    @patch('server.TCPServer.url_parser')
    @patch('server.requests')
    @patch('server.threading')
    @patch('server.TCPServer.workers')
    @patch('server.TCPServer.master')
    @patch('server.socket')
    def test_words_counter_multiple_urls(self, mock_socket, mock_master,
                           mock_workers, mock_threading,
                           mock_requests, mock_url_parser, mock_send_msg):
        text = 'а а а а а баобаб баобаб баобаб тук тук ту ту ту там там там пам пам пам пам'
        urls = ['example.com', 'anotherexample.com', 'thirdexample.com']
        client_socket = MagicMock()

        with patch('builtins.print') as mock_print:
            serv = server.TCPServer(1, 3)
            for url in urls:
                serv.words_counter(text, url, client_socket)

        expected_calls = [mock.call(client_socket, '{"а": 5, "пам": 4, "баобаб": 3}'),
                        mock.call( client_socket, '{"а": 5, "пам": 4, "баобаб": 3}'),
                        mock.call( client_socket, '{"а": 5, "пам": 4, "баобаб": 3}')]

        for i in range(len(urls)):
            self.assertEqual(expected_calls[i], mock_send_msg.call_args_list[i])

        self.assertEqual(mock_send_msg.call_count, 3)

if __name__ == '__main__':
    unittest.main()
