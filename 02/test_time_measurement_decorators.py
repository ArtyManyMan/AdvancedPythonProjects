"""This module contains a function 'my_function' and a decorator
'average_time_deco' for measuring and reporting
the average execution time of functions."""

import time
import unittest
from unittest import mock
from unittest.mock import patch
from time_measurement_decorators import my_function, average_time_deco


class TestAvgTimeDeco(unittest.TestCase):
    """A test case class for testing the 'my_function' function and 'average_time_deco' decorator."""

    def test_common_behavior_decorated_foo(self):
        for _ in range(11):
            self.assertEqual("Walter White! You're goddamn right", my_function("Walter"))

    def test_with_diff_types_params_for_avg_time_deco(self):

        for el in ['string', ['l', 's', 't'], (1,), {'a': 1, 'b': 2}, mock.Mock()]:

            @average_time_deco(el)
            def some_logic(arg_1, arg_2):
                res = arg_1 + arg_2
                time.sleep(1)
                return res

            with self.assertRaises(TypeError):
                some_logic("Walter", " White!")

    def test_decorator_print_calls_with_correct_values(self):
        """Test the behavior of the decorator regarding printed messages and average time."""

        call_num = 3

        @average_time_deco(call_num)
        def some_function():
            time.sleep(1)

        # сheck if the decorator prints the average time
        with patch('builtins.print') as mock_print:
            for _ in range(call_num):
                some_function()
                res = ' '.join(mock_print.call_args[0][0].split()[-2:])
                if _ < call_num - 1:
                    mock_print.assert_called_with(f'Среднее время выполнения последних {_ + 1} вызовов: ' + res)
                else:
                    mock_print.assert_called_with(f'Среднее время выполнения последних {call_num} вызовов: ' + res)
            self.assertEqual(call_num, mock_print.call_count)


    def test_decorator_with_insufficient_calls(self):
        @average_time_deco(3)
        def another_function():
            pass

        # сheck if the decorator prints a message when there are insufficient calls
        with patch('builtins.print') as mock_print:
            another_function()
            self.assertTrue(mock_print.called)
            last_print_call = mock_print.call_args[0][0]
        self.assertIn('Среднее время выполнения последних 1 вызовов: ', last_print_call)

        with patch('builtins.print') as mock_print:
            another_function()
            self.assertTrue(mock_print.called)
            last_print_call = mock_print.call_args[0][0]
        self.assertIn('Среднее время выполнения последних 2 вызовов: ', last_print_call)

    @patch('time.time')
    def test_decorator_time_calls(self, mock_time):
        """Test the decorator's behavior regarding time measurements."""

        call_num = 5

        @average_time_deco(call_num)
        def check_funk(*args):
            res = args[0] + " White! You're goddamn right"
            time.sleep(1)
            return res

        # сonfigure mock_time to return values
        mock_time.side_effect = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0]

        with patch('builtins.print') as mock_print:

            for i in range(call_num):
                self.assertEqual("Walter White! You're goddamn right", check_funk('Walter'))

        self.assertEqual(call_num*2, mock_time.call_count)
        self.assertEqual(call_num, mock_print.call_count)

        expected_calls_time = [mock.call()] * 10

        expected_calls_print = [
            mock.call('Среднее время выполнения последних 1 вызовов: 2.0 секунд'),
            mock.call('Среднее время выполнения последних 2 вызовов: 2.0 секунд'),
            mock.call('Среднее время выполнения последних 3 вызовов: 2.0 секунд'),
            mock.call('Среднее время выполнения последних 4 вызовов: 2.0 секунд'),
            mock.call(mock_print.call_args[0][0])
        ]

        mock_time.assert_has_calls(expected_calls_time)
        mock_print.assert_has_calls(expected_calls_print)
        self.assertEqual(expected_calls_print, mock_print.mock_calls)

    def test_avg_time_deco_zero_division(self):

        @average_time_deco(0)
        def check_funk(arg):
            res = arg + " White! You're goddamn right"
            time.sleep(1)
            return res

        with self.assertRaises(ZeroDivisionError):
            check_funk('Walter')

    def test_exception_handling(self):

        @average_time_deco(3)
        def function_with_exception():
            time.sleep(1)
            raise ValueError("Something went wrong")

        with patch('builtins.print') as mock_print:
            with self.assertRaises(ValueError):
                function_with_exception()

        # check if the exception was propagated upwards
        self.assertFalse(mock_print.called)


if __name__ == '__main__':
    unittest.main()
