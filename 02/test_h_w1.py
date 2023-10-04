"""Test the common behavior of the 'parse_json' function."""

import unittest
from unittest import mock
from unittest.mock import patch
from h_w1 import parse_json, func


class TestHW21(unittest.TestCase):
    """This class defines unit tests for the 'parse_json'
    and 'func' functions in the 'h_w21' module."""

    def setUp(self) -> None:
        self.json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        self.kit_required_fields = [["key1", "key2"], ["key1"],
                                    ["key3"], ["key2", "key3", "key4"],
                                    ["Key1", "keY2"], ["key2", "key2"]]

        self.kit_keywords = [["word2", 'word3'], ["word2", "word2", "word2", "word2"],
                             ["WORD", "WORLD", "WORD1"], ["WoRd3", "word4"],
                             ["", ""], ["W", " "]]

    @patch('h_w1.func', spec=func)
    def test_parse_json_common_behavior(self, mock_func):

        results = [["word2", 'word2', "word3"],
                   ["word2", "word2", "word2", "word2"],
                   [], ["WoRd3"], [], []]

        for i in range(6):
            self.assertEqual(None, parse_json(self.json_str, self.kit_required_fields[i], self.kit_keywords[i], mock_func))

            expected_calls = [mock.call(k) for k in results[i]]
            mock_func.assert_has_calls(expected_calls)
        self.assertEqual(len([j for i in results for j in i if j]), mock_func.call_count)

    @patch('h_w1.func', spec=func)
    def test_parse_json_with_dif_types(self, mock_func):
        json_str_variants = [1, ['{"key1": "Word1 word2"'], {1: 2, 2: 1},
                             None, 2.2, ('word', )]

        kit_required_fields = ['', [''], {1: 2, 2: 1}, ('abracadabra', ),
                               'some_string', {'mr.', 'Robot'}]

        kit_keywords = ['', [''], {1: 2, 2: 1}, ('abracadabra', ),
                        'some_string', {'mr.', 'Robot'}]

        for i in range(6):
            with self.assertRaises(TypeError):
                parse_json(json_str_variants[i], self.kit_required_fields[i], self.kit_keywords[i], func)

            self.assertEqual(None, parse_json(self.json_str, kit_required_fields[i], self.kit_keywords[i], func))

            self.assertEqual(None, parse_json(self.json_str, self.kit_required_fields[i], kit_keywords[i], func))

        self.assertIsNone(mock_func.assert_not_called())

    def test_keyword_callback_is_not_func(self):
        kit_keyword_callback = [1, ['{"key1": "Word1 word2"'],
                                {1: 2, 2: 1}, 2.2, ('word', ),
                                {'a', 'lunatic', 111}]

        kit_required_fields = ["key1", "key2", "key1",
                               "key2", "key1", "keY2"]

        kit_keywords = ["word2", 'word3', "word2",
                        "word2", "word2", "word2",
                        "WORD", "WORLD", "WORD1"]

        for i in range(6):
            with self.assertRaises(TypeError):
                parse_json(self.json_str, kit_required_fields,
                           kit_keywords, kit_keyword_callback[i])

    def test_wrong_register_keys(self):

        required_fields_1 = ["Key1", "keY2", "KEY1", "KEY2", "KEy2"]
        keywords = ['word2']

        self.assertEqual(None, parse_json(self.json_str, required_fields_1, keywords, mock.Mock()))

        json_str = '{"KEY1": "Word1 word2", "KEY2": "word2 word3"}'
        required_fields_2 = ["Key1", "keY2", "key1", "key2", "KEy2"]

        self.assertEqual(None, parse_json(json_str, required_fields_2, keywords, mock.Mock()))

    @patch('h_w1.func', spec=func)
    def test_wrong_register_values(self, mock_func):

        self.json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        required_fields = ["key1", "key2"]
        keywords = ["WORD1", "WORD2", "WORd1",
                    "WORd2", "wORD1", "wORD2",
                    "worD1", "WorD2", "WorD1"]

        results = ["WORD1", "WORD2", "WORd1",
                   "WORd2", "wORD1", "wORD2",
                   "worD1", "WorD2", "WorD1",
                   "WORD2", "WORd2", "wORD2",
                   "WorD2"]

        self.assertEqual(None, parse_json(self.json_str, required_fields, keywords, mock_func))

        self.assertEqual(13, mock_func.call_count)

        expected_calls = [mock.call(i) for i in results]

        self.assertIsNone(mock_func.assert_has_calls(expected_calls))


if __name__ == '__main__':
    unittest.main()
