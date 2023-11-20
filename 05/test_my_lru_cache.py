import unittest
from my_lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_common_behavior(self):

        lru_cache = LRUCache(2)

        lru_cache.set(1, 1)
        lru_cache.set(2, 2)

        self.assertEqual(1, lru_cache.get(1))

        lru_cache.set(3, 3)

        self.assertIsNone(lru_cache.get(2))

        lru_cache.set(4, 4)

        self.assertIsNone(lru_cache.get(1))

        self.assertEqual(3, lru_cache.get(3))
        self.assertEqual(4, lru_cache.get(4))

        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get("k3"))
        self.assertEqual("val2", cache.get("k2"))
        self.assertEqual("val1", cache.get("k1"))

        cache.set("k3", "val3")

        self.assertEqual("val3", cache.get("k3"))
        self.assertIsNone(cache.get("k2"))
        self.assertEqual("val1", cache.get("k1"))

    def test_wrong_limits(self):

        with self.assertRaisesRegex(ValueError, 'Limit should be int'):
            lru_cache = LRUCache(None)

        with self.assertRaisesRegex(ValueError, 'Limit should be int'):
            lru_cache = LRUCache('str')

        with self.assertRaisesRegex(ValueError, 'Limit should be int'):
            lru_cache = LRUCache(['just', 'lst', 1])

        with self.assertRaisesRegex(ValueError, 'Limit should be positive'):
            lru_cache = LRUCache(-1)

        with self.assertRaisesRegex(ValueError, 'Limit should be positive'):
            lru_cache = LRUCache(0)

        with self.assertRaisesRegex(ValueError, 'Limit should be positive'):
            lru_cache = LRUCache(-1000)

    def test_edge_low_limit(self):

        lru_cache = LRUCache(1)

        lru_cache.set(1, 1)
        self.assertEqual(1, lru_cache.get(1))
        lru_cache.set(2, 2)
        self.assertIsNone(lru_cache.get(1))
        self.assertEqual(2, lru_cache.get(2))

        lru_cache.set(3, 3)
        self.assertIsNone(lru_cache.get(1))
        self.assertIsNone(lru_cache.get(2))
        self.assertEqual(3, lru_cache.get(3))

        lru_cache.set(4, 4)

        self.assertIsNone(lru_cache.get(1))
        self.assertIsNone(lru_cache.get(2))
        self.assertIsNone(lru_cache.get(3))
        self.assertEqual(4, lru_cache.get(4))

    def test_get_and_set_with_limit_3(self):

        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        self.assertEqual("val1", cache.get("k1"))
        self.assertEqual("val2", cache.get("k2"))
        self.assertEqual("val3", cache.get("k3"))

        cache.set("k4", "val4")
        self.assertIsNone(cache.get("k1"))
        self.assertEqual("val2", cache.get("k2"))
        self.assertEqual("val3", cache.get("k3"))
        self.assertEqual("val4", cache.get("k4"))

        cache.set("k5", "val5")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual("val3", cache.get("k3"))
        self.assertEqual("val4", cache.get("k4"))
        self.assertEqual("val5", cache.get("k5"))

        cache.set("k6", "val6")
        self.assertIsNone(cache.get("k3"))
        self.assertEqual("val4", cache.get("k4"))
        self.assertEqual("val5", cache.get("k5"))
        self.assertEqual("val6", cache.get("k6"))

    def test_get_and_set_with_limit_5(self):

        new_cache = LRUCache(5)

        new_cache.set("k5", "val5")
        new_cache.set("k4", "val4")
        new_cache.set("k3", "val3")
        new_cache.set("k2", "val2")
        new_cache.set("k1", "val1")

        self.assertEqual("val5", new_cache.get("k5"))
        self.assertEqual("val4", new_cache.get("k4"))
        self.assertEqual("val3", new_cache.get("k3"))
        self.assertEqual("val2", new_cache.get("k2"))
        self.assertEqual("val1", new_cache.get("k1"))

        new_cache.set("k0", "val0")

        self.assertIsNone(new_cache.get("k5"))
        self.assertEqual("val0", new_cache.get("k0"))
        self.assertEqual("val1", new_cache.get("k1"))
        self.assertEqual("val2", new_cache.get("k2"))
        self.assertEqual("val3", new_cache.get("k3"))
        self.assertEqual("val4", new_cache.get("k4"))

        new_cache.set("k5", "val5")
        self.assertIsNone(new_cache.get("k0"))
        self.assertEqual("val5", new_cache.get("k5"))

    def test_get_and_set_with_limit_7(self):

        new_cache = LRUCache(7)

        new_cache.set("k7", "val7")
        new_cache.set("k6", "val6")
        new_cache.set("k5", "val5")
        new_cache.set("k4", "val4")
        new_cache.set("k3", "val3")
        new_cache.set("k2", "val2")
        new_cache.set("k1", "val1")

        self.assertEqual("val7", new_cache.get("k7"))
        self.assertEqual("val6", new_cache.get("k6"))
        self.assertEqual("val5", new_cache.get("k5"))
        self.assertEqual("val4", new_cache.get("k4"))
        self.assertEqual("val3", new_cache.get("k3"))
        self.assertEqual("val2", new_cache.get("k2"))
        self.assertEqual("val1", new_cache.get("k1"))

        new_cache.set("k0", "val0")

        self.assertIsNone(new_cache.get("k7"))
        self.assertEqual("val0", new_cache.get("k0"))
        self.assertEqual("val1", new_cache.get("k1"))
        self.assertEqual("val2", new_cache.get("k2"))
        self.assertEqual("val3", new_cache.get("k3"))
        self.assertEqual("val4", new_cache.get("k4"))
        self.assertEqual("val5", new_cache.get("k5"))
        self.assertEqual("val6", new_cache.get("k6"))

        new_cache.set("k7", "val7")
        self.assertIsNone(new_cache.get("k0"))
        self.assertEqual("val7", new_cache.get("k7"))

    def test_set_and_get_cases(self):

        cache = LRUCache(3)

        with self.assertRaisesRegex(ValueError, "Value can't be None"):
            cache.set("k1", None)
        cache.set("k2", "val2")
        self.assertIsNone(cache.get("k1"))

        self.assertIsNone(cache.get("k1"))
        self.assertEqual("val2", cache.get("k2"))

        cache.set("k3", "val3")

        self.assertEqual("val3", cache.get("k3"))
        self.assertEqual("val2", cache.get("k2"))

        with self.assertRaisesRegex(ValueError, "Value can't be None"):
            cache.set("k1", None)
        self.assertEqual("val2", cache.get("k2"))
        self.assertEqual("val3", cache.get("k3"))
        self.assertIsNone(cache.get("k1"))

        cache.set("k4", "val4")
        cache.set("k5", "val5")

        self.assertIsNone(cache.get("k2"))
        self.assertEqual("val3", cache.get("k3"))
        self.assertEqual("val4", cache.get("k4"))
        self.assertEqual("val5", cache.get("k5"))

        with self.assertRaisesRegex(TypeError, "unhashable type: 'list'"):
            cache.set(["l", "i", "s", "t"], ['of str'])
        with self.assertRaisesRegex(TypeError, "unhashable type: 'set'"):
            cache.set({"l", "i", "s", "t"}, ['of str'])
        with self.assertRaisesRegex(TypeError, "unhashable type: 'dict'"):
            cache.set({"l": "i", "s": "t"}, ['of str'])
        with self.assertRaisesRegex(ValueError, "Value can't be None"):
            cache.set(["l", "i", "s", "t"], None)
        with self.assertRaisesRegex(ValueError, "Value can't be None"):
            cache.set({"l", "i", "s", "t"}, None)
        with self.assertRaisesRegex(ValueError, "Value can't be None"):
            cache.set({"l": "i", "s": "t"}, None)

        with self.assertRaisesRegex(TypeError, "unhashable type: 'list'"):
            cache.get(["l", "i", "s", "t"])
        with self.assertRaisesRegex(TypeError, "unhashable type: 'set'"):
            cache.get({"l", "i", "s", "t"})
        with self.assertRaisesRegex(TypeError, "unhashable type: 'dict'"):
            self.assertIsNone(cache.get({"l": "i", "s": "t"}))

        self.assertEqual("val3", cache.get("k3"))
        self.assertEqual("val4", cache.get("k4"))
        self.assertEqual("val5", cache.get("k5"))

    def test_set_with_switch_values(self):

        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k2", "other_val2")

        self.assertEqual("val1", cache.get("k1"))
        self.assertEqual("other_val2", cache.get("k2"))
        cache.set("k3", "val3")

        self.assertEqual("val3", cache.get("k3"))

        cache.set("k1", "other val1")
        cache.set("k4", "val4")

        self.assertIsNone(cache.get("k2"))
        self.assertEqual("other val1", cache.get("k1"))
        self.assertEqual("val3", cache.get("k3"))
        self.assertEqual("val4", cache.get("k4"))

    def test_out_of_expected_api(self):

        cache = LRUCache(3)

        self.assertEqual(3, cache._LRUCache__limit)
        self.assertEqual({}, cache._LRUCache__cache_table)

        cache.set("k1", "val1")
        self.assertEqual(1, len(cache._LRUCache__cache_table))

        self.assertEqual({"k1": "val1"}, cache._LRUCache__cache_table)

        cache.set("k2", "val2")
        self.assertEqual(2, len(cache._LRUCache__cache_table))

        self.assertEqual({"k1": "val1", "k2": "val2"}, cache._LRUCache__cache_table)

        cache.set("k3", "val3")
        self.assertEqual(3, len(cache._LRUCache__cache_table))

        self.assertEqual({"k1": "val1", "k2": "val2", "k3": "val3"}, cache._LRUCache__cache_table)

        self.assertEqual(3, cache._LRUCache__limit)

        cache.set("k4", "val4")
        self.assertEqual(3, len(cache._LRUCache__cache_table))

        self.assertEqual({"k2": "val2", "k3": "val3", "k4": "val4"}, cache._LRUCache__cache_table)

        self.assertIsNone(cache.get("k1"))

        self.assertEqual("val2", cache.get("k2"))
        self.assertEqual("val3", cache.get("k3"))
        self.assertEqual("val4", cache.get("k4"))


if __name__ == '__main__':
    unittest.main()
