import unittest
import json
import cjson

class TestJSONMethods(unittest.TestCase):

    def test_loads(self):
        json_str = '{"hello": "10", "world": "val"}'
        python_dict = {"hello": "10", "world": "val"}
        self.assertEqual(cjson.loads(json_str), python_dict)
        self.assertEqual(cjson.loads(json_str), json.loads(json_str))

        json_str = '{"hello": 10, "world": "val"}'
        python_dict = {'hello': 10, 'world': 'val'}
        self.assertEqual(cjson.loads(json_str), python_dict)
        self.assertEqual(cjson.loads(json_str), json.loads(json_str))

        json_str = '{10: "10", 20: "val"}'
        result = {'10': '10', '20': 'val'}

        self.assertEqual(cjson.loads(json_str), result)


    def test_empty_loads(self):
        json_str = '{}'

        self.assertEqual(cjson.loads(json_str), {})
        self.assertEqual(cjson.loads(json_str), json.loads(json_str))

    def test_dumps(self):
        python_dict = {"hello": "10", "world": "value"}
        result = '{"hello": "10", "world": "value"}'
        self.assertEqual(cjson.dumps(python_dict), json.dumps(python_dict))
        self.assertEqual(cjson.dumps(python_dict), result)

        python_dict = {"hello": 10, "world": "value"}
        result = '{"hello": 10, "world": "value"}'
        self.assertEqual(cjson.dumps(python_dict), result)
        self.assertEqual(cjson.dumps(python_dict), json.dumps(python_dict))

        python_dict = {10: "hello", "world": "value"}
        result = '{10: "hello", "world": "value"}'
        self.assertEqual(cjson.dumps(python_dict), result)

    def test_empty_dumps(self):

        python_dict = {}

        self.assertEqual(cjson.dumps(python_dict), '{}')
        self.assertEqual(cjson.dumps(python_dict), json.dumps(python_dict))

    def test_string_keys_with_string_or_number_values(self):

        json_str = '{"key1": "value1", "key2": 10, "key3": "value3", "key4": 20}'
        python_dict = {"key1": "value1", "key2": 10, "key3": "value3", "key4": 20}
        self.assertEqual(cjson.loads(json_str), python_dict)
        self.assertEqual(cjson.loads(json_str), json.loads(json_str))

        json_str = '{"key5": 30, "key6": "value6", "key7": 40, "key8": "value8"}'
        python_dict = {"key5": 30, "key6": "value6", "key7": 40, "key8": "value8"}
        self.assertEqual(cjson.loads(json_str), python_dict)
        self.assertEqual(cjson.loads(json_str), json.loads(json_str))

        json_str = '{"key9": "value9", "key10": "10", "key11": 20}'
        python_dict = {"key9": "value9", "key10": "10", "key11": 20}
        self.assertEqual(cjson.loads(json_str), python_dict)
        self.assertEqual(cjson.loads(json_str), json.loads(json_str))

if __name__ == '__main__':
    unittest.main()
