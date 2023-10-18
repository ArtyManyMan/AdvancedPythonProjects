"""This module contains unit tests for
the CustomList class in the `list_heir` module."""

import unittest
from list_heir import CustomList


class TestCustomList(unittest.TestCase):

    def test_add(self):

        var1 = CustomList([6, 3, 10, 7])
        var2 = CustomList([5, 1, 3, 7])
        var3 = CustomList([1, 2, 7])

        self.assertEqual(var1, var2 + var3)
        self.assertEqual(var2, CustomList([5, 1, 3, 7]))
        self.assertEqual(var3, CustomList([1, 2, 7]))

        var1 = CustomList([3, 5])
        var2 = CustomList([1])
        var3 = [2, 5]

        self.assertEqual(var1, var2 + var3)
        self.assertEqual(var2, CustomList([1]))

        self.assertEqual(var1, var3 + var2)
        self.assertEqual(var2, CustomList([1]))

    def test_add_with_empty_list(self):
        custom_list1 = CustomList([1, 2, 3, 4, 5])
        custom_list2 = CustomList([])

        result1 = custom_list1 + custom_list2

        result2 = custom_list1 + []

        self.assertEqual(CustomList([1, 2, 3, 4, 5]), result1)
        self.assertEqual(CustomList([1, 2, 3, 4, 5]), result2)

        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list2, CustomList([]))

    def test_sub(self):

        var1 = CustomList([4, -1, -4, 7])
        var2 = CustomList([5, 1, 3, 7])
        var3 = CustomList([1, 2, 7])

        self.assertEqual(var1, var2 - var3)
        self.assertEqual(var2, CustomList([5, 1, 3, 7]))
        self.assertEqual(var3, CustomList([1, 2, 7]))

        var1 = CustomList([-1, -5])
        var2 = CustomList([1])
        var3 = [2, 5]

        self.assertEqual(var1, var2 - var3)
        self.assertEqual(var2, CustomList([1]))
        self.assertEqual(var3, [2, 5])

        var1 = CustomList([1, 5])
        var2 = [2, 5]
        var3 = CustomList([1])

        self.assertEqual(var1, var2 - var3)
        self.assertEqual(var3, CustomList([1]))
        self.assertEqual(var2, [2, 5])

    def test_sub_with_empty_list(self):

        custom_list1 = CustomList([1, 2, 3, 4, 5])
        custom_list2 = CustomList([])

        result1 = custom_list1 - custom_list2

        result2 = custom_list1 - []

        self.assertEqual(CustomList([1, 2, 3, 4, 5]), result1)
        self.assertEqual(CustomList([1, 2, 3, 4, 5]), result2)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list2, CustomList([]))

    def test_comparison(self):
        self.assertTrue(CustomList([5, 5, 17]) == CustomList([10, 7, 3, 7]))
        self.assertTrue(CustomList([10, 7, 3]) <= CustomList([5, 5, 17]))
        self.assertTrue(CustomList([10, 7, 3, 7]) >= CustomList([5, 5, 1, 1, 1, 7, 7]))
        self.assertTrue(CustomList([10, 7, 3]) < CustomList([5, 5, 1, 1, 1, 7, 7]))
        self.assertTrue(CustomList([10, 7]) > CustomList([5]))
        self.assertTrue(CustomList([10, 7]) != CustomList([5]))
        self.assertFalse(CustomList([10, 7]) != CustomList([5, 12]))

    def test_inheritance_of_list_behavior(self):
        custom_list1 = CustomList([5, 5, 17])
        custom_list2 = CustomList([5, 5])
        custom_list2.append(17)

        self.assertEqual(custom_list1, custom_list1)

        self.assertEqual(5, custom_list2.pop(0))

        custom_list1.extend([0, 1, 2, 7, 11])
        self.assertEqual(CustomList([5, 5, 17, 0, 1, 2, 7, 11]), custom_list1)

        self.assertEqual(2, custom_list1.count(5))

        self.assertEqual(3, custom_list1.index(0))

        custom_list1.reverse()
        self.assertEqual(CustomList([11, 7, 2, 1, 0, 17, 5, 5]), custom_list1)

        custom_list1.remove(5)
        self.assertEqual(CustomList([11, 7, 2, 1, 0, 17, 5]), custom_list1)
        self.assertEqual(CustomList([2, 1, 0]), custom_list1[2:5])

        custom_list1 = [0, 4, 1, 2, 7, 11]
        self.assertEqual(CustomList([7, 2, 1]), custom_list1[-2:-5:-1])

    def test_str_with_non_empty_list(self):
        custom_list1 = CustomList([1, 2, 3, 4, 5])
        custom_list2 = CustomList([0])

        self.assertEqual('CustomList([1, 2, 3, 4, 5]) сумма элементов = 15', str(custom_list1))
        self.assertEqual('CustomList([0]) сумма элементов = 0', str(custom_list2))

    def test_str_with_empty_list(self):
        custom_list = CustomList([])
        result = str(custom_list)
        self.assertEqual(result, 'CustomList([]) список пуст')

    def test_len_custom_list(self):
        custom_list1 = CustomList([5, 5, 17])

        self.assertEqual(3, len(custom_list1))

        custom_list2 = CustomList([])
        self.assertEqual(0, len(custom_list2))

        custom_list1.append(10)
        self.assertEqual(4, len(custom_list1))

        custom_list1.pop()
        self.assertEqual(3, len(custom_list1))

    def test_sorting(self):
        custom_list = CustomList([5, 1, 3, 7, 2])

        custom_list.sort()
        self.assertEqual(CustomList([1, 2, 3, 5, 7]), custom_list)

    def test_exceptions(self):
        custom_list = CustomList([1, 2, 3])

        with self.assertRaises(IndexError):
            result = custom_list[10]

        with self.assertRaises(TypeError):
            result = custom_list / 0

    def test_add_custom_list_with_different_sizes(self):
        custom_list1 = CustomList([1, 2, 3, 4, 5])
        custom_list2 = CustomList([1, 2, 3])

        result1 = custom_list1 + custom_list2
        self.assertEqual(CustomList([2, 4, 6, 4, 5]), result1)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list2, CustomList([1, 2, 3]))

        result2 = custom_list2 + custom_list1
        self.assertEqual(CustomList([2, 4, 6, 4, 5]), result2)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list2, CustomList([1, 2, 3]))

        custom_list3 = CustomList([1, 2])
        result3 = custom_list1 + custom_list3
        self.assertEqual(CustomList([2, 4, 3, 4, 5]), result3)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list3, CustomList([1, 2]))

        result4 = custom_list3 + custom_list1
        self.assertEqual(CustomList([2, 4, 3, 4, 5]), result4)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list3, CustomList([1, 2]))

    def test_add_custom_and_regular_list_with_different_sizes(self):
        custom_list = CustomList([1, 2, 3, 4, 5])
        regular_list = [1, 2, 3]

        result1 = custom_list + regular_list
        self.assertEqual(CustomList([2, 4, 6, 4, 5]), result1)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))

        result2 = regular_list + custom_list
        self.assertEqual(CustomList([2, 4, 6, 4, 5]), result2)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))

        regular_list2 = [1, 2]
        result3 = custom_list + regular_list2
        self.assertEqual(CustomList([2, 4, 3, 4, 5]), result3)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))

        result4 = regular_list2 + custom_list
        self.assertEqual(CustomList([2, 4, 3, 4, 5]), result4)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))

    def test_sub_custom_list_with_different_sizes(self):
        custom_list1 = CustomList([1, 2, 3, 4, 5])
        custom_list2 = CustomList([1, 2, 3])

        result1 = custom_list1 - custom_list2
        self.assertEqual(CustomList([0, 0, 0, 4, 5]), result1)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list2, CustomList([1, 2, 3]))

        result2 = custom_list2 - custom_list1
        self.assertEqual(CustomList([0, 0, 0, -4, -5]), result2)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list2, CustomList([1, 2, 3]))

        custom_list3 = CustomList([1, 2])
        result3 = custom_list1 - custom_list3
        self.assertEqual(CustomList([0, 0, 3, 4, 5]), result3)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list3, CustomList([1, 2]))

        result4 = custom_list3 - custom_list1
        self.assertEqual(CustomList([0, 0, -3, -4, -5]), result4)
        self.assertEqual(custom_list1, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(custom_list3, CustomList([1, 2]))

    def test_sub_custom_and_regular_list_with_different_sizes(self):
        custom_list = CustomList([1, 2, 3, 4, 5])
        regular_list = [1, 2, 3]

        result1 = custom_list - regular_list
        self.assertEqual(CustomList([0, 0, 0, 4, 5]), result1)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(regular_list, [1, 2, 3])

        result2 = regular_list - custom_list
        self.assertEqual(CustomList([0, 0, 0, -4, -5]), result2)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(regular_list, [1, 2, 3])

        regular_list2 = [1, 2]
        result3 = custom_list - regular_list2
        self.assertEqual(CustomList([0, 0, 3, 4, 5]), result3)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(regular_list, [1, 2, 3])

        result4 = regular_list2 - custom_list
        self.assertEqual(CustomList([0, 0, -3, -4, -5]), result4)
        self.assertEqual(custom_list, CustomList([1, 2, 3, 4, 5]))
        self.assertEqual(regular_list, [1, 2, 3])

if __name__ == '__main__':
    unittest.main()
