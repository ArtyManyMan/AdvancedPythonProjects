"""This module defines the `CustomList` class,
which is a custom extension of the Python `list` class.
It provides additional functionality for element-wise addition,
subtraction, comparison, and a custom string representation."""

class CustomList(list):

    def __add__(self, other):
        if not isinstance(other, CustomList):
            other = CustomList(other)

        counter = max(len(self), len(other))
        result = []
        for i in range(counter):
            term1 = self[i] if i < len(self) else 0
            term2 = other[i] if i < len(other) else 0
            result.append(term1 + term2)
        return CustomList(result)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not isinstance(other, CustomList):
            other = CustomList(other)

        counter = max(len(self), len(other))
        result = []
        for i in range(counter):
            term1 = self[i] if i < len(self) else 0
            term2 = other[i] if i < len(other) else 0
            result.append(term1 - term2)
        return CustomList(result)

    def __rsub__(self, other):
        if not isinstance(other, CustomList):
            other = CustomList(other)

        return other.__sub__(self)

    @staticmethod
    def sum_centr(arg1, arg2):
        return sum(arg1), sum(arg2)

    def __eq__(self, other):
        arg1, arg2 = self.sum_centr(self, other)
        return arg1 == arg2

    def __ne__(self, other):
        arg1, arg2 = self.sum_centr(self, other)
        return arg1 != arg2

    def __le__(self, other):
        arg1, arg2 = self.sum_centr(self, other)
        return arg1 <= arg2

    def __ge__(self, other):
        arg1, arg2 = self.sum_centr(self, other)
        return arg1 >= arg2

    def __gt__(self, other):
        arg1, arg2 = self.sum_centr(self, other)
        return arg1 > arg2

    def __lt__(self, other):
        arg1, arg2 = self.sum_centr(self, other)
        return arg1 < arg2

    def __str__(self):
        if not self:
            return f'CustomList({list(self)}) список пуст'
        return f'CustomList({list(self)}) сумма элементов = {sum(self)}'
