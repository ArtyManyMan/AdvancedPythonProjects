"""Test the common behavior of the 'parse_json' function."""

import unittest
from unittest import mock
from unittest.mock import patch
from json_parser_utils import parse_json, func


class TestParsJson(unittest.TestCase):
    """This class defines unit tests for the 'parse_json'
    and 'func' functions in the 'json_parser_utils' module."""

    @patch('json_parser_utils.func', spec=func)
    def test_parse_json_common_behavior(self, mock_func):

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        kit_required_fields = [["key1", "key2"], ["key1"],
                               ["key3"], ["key2", "key3", "key4"],
                               ["Key1", "keY2"], ["key2", "key2"]]

        kit_keywords = [["word2", 'word3'], ["word2", "word2", "word2", "word2"],
                        ["WORD", "WORLD", "WORD1"], ["WoRd3", "word4"],
                        ["", ""], ["W", " "]]

        results = [[("key1", "word2"), ("key2", "word2"), ("key2", "word3")],
                   [("key1", "word2"), ("key1", "word2"), ("key1", "word2"), ("key1", "word2")],
                   [], [("key2", "WoRd3")], [], []]

        for i in range(6):
            self.assertEqual(None, parse_json(json_str, kit_required_fields[i], kit_keywords[i], mock_func))

            expected_calls = [mock.call(*k) for k in results[i]]

            mock_func.assert_has_calls(expected_calls)

        self.assertEqual(len([j for res in results for j in res if j]), mock_func.call_count)

    @patch('json_parser_utils.func', spec=func)
    def test_parser_json_str_with_dif_types(self, mock_func):

        json_str_variants = [1, ['{"key1": "Word1 word2"'], {1: 2, 2: 1},
                             None, 2.2, ('word',)]

        kit_required_fields = [["key1", "key2"], ["key1"],
                               ["key3"], ["key2", "key3", "key4"],
                               ["Key1", "keY2"], ["key2", "key2"]]

        kit_keywords = [["word2", 'word3'], ["word2", "word2", "word2", "word2"],
                        ["WORD", "WORLD", "WORD1"], ["WoRd3", "word4"],
                        ["", ""], ["W", " "]]

        for i in range(6):
            with self.assertRaises(TypeError):
                parse_json(json_str_variants[i], kit_required_fields[i], kit_keywords[i], func)

        self.assertIsNone(mock_func.assert_not_called())

    @patch('json_parser_utils.func', spec=func)
    def test_parser_json_required_fields_with_dif_types(self, mock_func):

        json_str_def = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        kit_required_fields_variants = ['', [''], {1: 2, 2: 1}, ('abracadabra',),
                                        'some_string', {'mr.', 'Robot'}]

        kit_keywords = [["word2", 'word3'], ["word2", "word2", "word2", "word2"],
                        ["WORD", "WORLD", "WORD1"], ["WoRd3", "word4"],
                        ["", ""], ["W", " "]]

        for i in range(6):

            self.assertEqual(None, parse_json(json_str_def, kit_required_fields_variants[i], kit_keywords[i], func))

        self.assertIsNone(mock_func.assert_not_called())

    @patch('json_parser_utils.func', spec=func)
    def test_parser_json_keywords_with_dif_types(self, mock_func):

        json_str_def = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        kit_required_fields = [["key1", "key2"], ["key1"],
                               ["key3"], ["key2", "key3", "key4"],
                               ["Key1", "keY2"], ["key2", "key2"]]

        kit_keywords_variants = ['', [''], {1: 2, 2: 1}, ('abracadabra',),
                                 'some_string', {'mr.', 'Robot'}]

        for i in range(6):

            self.assertEqual(None, parse_json(json_str_def, kit_required_fields[i], kit_keywords_variants[i], func))

        self.assertIsNone(mock_func.assert_not_called())

    def test_keyword_callback_is_not_func(self):

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        kit_required_fields = ["key1", "key2", "key1",
                               "key2", "key1", "keY2"]

        kit_keywords = ["word2", 'word3', "word2",
                        "word2", "word2", "word2",
                        "WORD", "WORLD", "WORD1"]

        kit_keyword_callback = [1, ['{"key1": "Word1 word2"'],
                                {1: 2, 2: 1}, 2.2, ('word',),
                                {'a', 'lunatic', 111}]

        for i in range(6):
            with self.assertRaises(TypeError):
                parse_json(json_str, kit_required_fields, kit_keywords, kit_keyword_callback[i])


    def test_wrong_register_keys(self):

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_fields_1 = ["Key1", "keY2", "KEY1", "KEY2", "KEy2"]
        keywords = ['word2']

        self.assertEqual(None, parse_json(json_str, required_fields_1, keywords, mock.Mock()))

        json_str = '{"KEY1": "Word1 word2", "KEY2": "word2 word3"}'
        required_fields_2 = ["Key1", "keY2", "key1", "key2", "KEy2"]

        self.assertEqual(None, parse_json(json_str, required_fields_2, keywords, mock.Mock()))

    @patch('json_parser_utils.func', spec=func)
    def test_upper_lower_register_values(self, mock_func):

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        required_fields = ["key1", "key2"]
        keywords = ["WORD1", "WORD2", "WORd1",
                    "WORd2", "wORD1", "wORD2",
                    "worD1", "WorD2", "WorD1"]

        results = [("key1", "WORD1"), ("key1", "WORD2"), ("key1", "WORd1"),
                   ("key1", "WORd2"), ("key1", "wORD1"), ("key1", "wORD2"),
                   ("key1", "worD1"), ("key1", "WorD2"), ("key1", "WorD1"),
                   ("key2", "WORD2"), ("key2", "WORd2"), ("key2", "wORD2"),
                   ("key2", "WorD2")]

        self.assertEqual(None, parse_json(json_str, required_fields, keywords, mock_func))

        self.assertEqual(13, mock_func.call_count)

        expected_calls = [mock.call(*i) for i in results]

        self.assertIsNone(mock_func.assert_has_calls(expected_calls))

    @patch('json_parser_utils.func', spec=func)
    def test_multiple_keywords(self, mock_func):

        json_str = '{"key1": "Word1 word2", "key2": "word2 word3", "key3": "word2 word2"}'

        required_fields = ["key1", "key2", "key3"]
        keywords = ["word2", "word3"]

        # Ожидаемые результаты для каждого вызова колбека
        results = [("key1", "word2"), ("key2", "word2"), ("key2", "word3"), ("key3", "word2")]

        self.assertEqual(None, parse_json(json_str, required_fields, keywords, mock_func))

        expected_calls = [mock.call("key1", "word2"), mock.call("key2", "word2"),
                          mock.call ("key2", "word3"), mock.call("key3", "word2")]

        mock_func.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(len(results), mock_func.call_count)

    @patch('json_parser_utils.func', spec=func)
    def test_missing_keyword(self, mock_func):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3", "key3": "word2 word2"}'

        required_fields = ["key1", "key2", "key3"]
        keywords = ["missed_keyword"]

        self.assertEqual(None, parse_json(json_str, required_fields, keywords, func))
        mock_func.assert_not_called()

    @patch('json_parser_utils.func', spec=func)
    def test_multiple_keywords_in_single_line(self, mock_func):

        json_str = '{"key1": "Word1 word2 word3 word4", "key2": "word4 word1 word2"}'

        required_fields = ["key1", "key2", "key3"]
        keywords = ["word2", "word3", "word4"]

        results = [("key1", "word2"), ("key1", "word3"), ("key1", "word4"),
                   ("key2", "word4"), ("key2", "word2")]

        self.assertEqual(None, parse_json(json_str, required_fields, keywords, mock_func))

        expected_calls = [mock.call("key1", "word2"), mock.call("key1", "word3"),
                          mock.call("key1", "word4"), mock.call("key2", "word2"),
                          mock.call("key2", "word4"),]

        mock_func.assert_has_calls(expected_calls)
        self.assertEqual(len(results), mock_func.call_count)

if __name__ == '__main__':
    unittest.main()
