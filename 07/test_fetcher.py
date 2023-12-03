import asyncio
import unittest
from unittest.mock import MagicMock, patch, AsyncMock, mock_open, call
import fetcher


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    @patch("fetcher.argparse")
    async def test_fetch_valid_url(self, mock_argparse):
        mock_response = MagicMock()
        mock_response.status = 200

        mock_get = MagicMock()
        mock_get.__aenter__.return_value = mock_response

        mock_session = MagicMock()
        mock_session.get = MagicMock(return_value=mock_get)

        with patch("fetcher.aiohttp.ClientSession") as mock_client_session:
            mock_client_session.return_value.__aenter__.return_value = mock_session

            valid_url = "http://example.com"
            expected_result = 200

            result = await fetcher.fetch(valid_url)

            self.assertEqual(result, expected_result)

    @patch("fetcher.argparse")
    async def test_fetch_invalid_url(self, mock_argparse):
        invalid_url = "http://invalidurl"

        result = await fetcher.fetch(invalid_url)

        self.assertEqual(
            result,
            "Connection problem: Cannot connect to host invalidurl:80 ssl:default [Temporary failure in name resolution]",
        )

    async def test_main_function(self):
        workers_num = 5

        file_content = [
            "http://test1.ru",
            "http://test2.ru",
            "http://test3.ru",
            "http://test4.ru",
            "http://test5.ru",
        ]

        async def mocked_fetch(url):
            return 200

        with patch(
            "fetcher.fetch", new=AsyncMock(side_effect=mocked_fetch)
        ) as mock_fetch:
            with patch(
                "fetcher.open", new=mock_open(read_data="\n".join(file_content))
            ) as file_data:
                with patch("builtins.print") as mock_print:
                    await fetcher.main(workers_num)

        expected_calls = [
            call(
                "Обработано 1 URLs. http://test1.ru status code is 200. Worker number 0."
            ),
            call(
                "Обработано 2 URLs. http://test2.ru status code is 200. Worker number 0."
            ),
            call(
                "Обработано 3 URLs. http://test3.ru status code is 200. Worker number 0."
            ),
            call(
                "Обработано 4 URLs. http://test4.ru status code is 200. Worker number 0."
            ),
            call(
                "Обработано 5 URLs. http://test5.ru status code is 200. Worker number 0."
            ),
        ]

        self.assertEqual(5, mock_print.call_count)
        self.assertEqual(expected_calls, mock_print.call_args_list)

        expected_calls = [
            call("http://test1.ru"),
            call("http://test2.ru"),
            call("http://test3.ru"),
            call("http://test4.ru"),
            call("http://test5.ru")
        ]

        self.assertIsNone(mock_fetch.assert_has_awaits(expected_calls))
        self.assertEqual(5, mock_fetch.call_count)


    async def test_worker_with_handmade_que(self):
        file_content = [
            "http://test1.ru",
            "http://test2.ru",
            "http://test3.ru",
            "http://test4.ru",
            "http://test5.ru",
        ]

        que = asyncio.Queue()
        for i in file_content:
            que.put_nowait(i)

        with patch(
            "fetcher.open", new=mock_open(read_data="\n".join(file_content))
        ) as mock_file:
            with patch("fetcher.asyncio.Queue", side_effect=que):
                with patch("fetcher.fetch", return_value=200) as mock_fetch:
                    with patch("builtins.print") as mock_print:
                        await fetcher.worker(que, 0)

        self.assertEqual(5, mock_fetch.call_count)

    async def test_worker(self):

        mock_queue = AsyncMock(spec=asyncio.Queue)
        mock_queue.get.return_value = "http://test1.ru"
        mock_queue.empty.side_effect = [False, True]

        with patch("fetcher.asyncio.Queue", new=mock_queue) as que:
            with patch('fetcher.fetch', return_value=200):
                with patch('builtins.print') as mock_print:
                    await fetcher.worker(mock_queue, 0)

        self.assertEqual(2, que.empty.call_count)
        self.assertEqual(1, que.get.call_count)

        self.assertEqual([call()], que.get.call_args)


if __name__ == "__main__":
    unittest.main()
