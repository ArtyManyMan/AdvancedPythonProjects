"""
Unit tests for the 'gen' function in the 'home_work_ex2' module.
"""

import unittest
from unittest.mock import MagicMock
from file_filter import gen
import io


class TestGen(unittest.TestCase):
    def test_find_single_word(self):

        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['а Розаа упала на лапу Азора',
                                           'разора азора ароза и роза зорара',
                                           'раз о розалин РОСАТОМ роз а']
        lst = ['роза']

        result = list(gen(mock_file, lst))

        self.assertEqual(result, ['разора азора ароза и роза зорара'])

    def test_find_some_words(self):

        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['а Розаа упала на лапу Азора',
                                           'разора азора ароза и роза зорара',
                                           'раз о розалин РОСАТОМ роз а',
                                           'РОЗА', 'рОзА']

        lst = ['роза']

        result = list(gen(mock_file, lst))

        self.assertEqual(result, ['разора азора ароза и роза зорара',
                                  'РОЗА', 'рОзА'])

    def test_find_zero_words(self):

        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['а Розаа упала на лапу Азора',
                                           'разора азора ароза и розаа зорара',
                                           'раз о розалин РОСАТОМ роз а',
                                           'РОЗАо', 'рОзАы']

        lst = ['роза']
        result = list(gen(mock_file, lst))

        self.assertEqual(result, [])

    def test_for_different_decoding(self):

        mock_file_cp1251 = MagicMock(spec=io.TextIOWrapper)
        mock_file_cp1251.__iter__.return_value = [i.encode('cp1251')
                                                  for i in ['а ПРозаК упала на лапу Азора',
                                                            'разора азора ароза и роза зорара',
                                                            'раз о розалин РОСАТОМ роз а',
                                                            'УГРОЗА', 'рОзАЗИЗУ']]

        mock_file_koi8r = MagicMock(spec=io.TextIOWrapper)
        mock_file_koi8r.__iter__.return_value = [i.encode('KOI8-R')
                                                 for i in ['а ПРозаК упала на лапу Азора',
                                                           'разора азора ароза и роза зорара',
                                                           'раз о розалин РОСАТОМ роз а',
                                                           'УГРОЗА', 'рОзАЗИЗУ']]

        lst = ['роза']

        result_cp1251 = list(gen(mock_file_cp1251, lst))

        result_koi8r = list(gen(mock_file_koi8r, lst))

        self.assertEqual(result_cp1251, [])
        self.assertEqual(result_koi8r, [])

    def test_uncorrect_input_first_arg(self):
        invalid_inputs = [1, 2.0, [], {}]
        lst = ['test']

        for i in invalid_inputs:
            with self.assertRaises(TypeError):
                for _ in gen(i, lst):
                    pass

    def test_uncorrect_input_second_arg(self):
        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['а Розаа упала на лапу Азора',
                                           'разора азора ароза и розаа зорара',
                                           'раз о розалин РОСАТОМ роз а',
                                           'РОЗАо', 'рОзАы']

        uncorrect_input_lists = [[1, 2, 3], [{}, (1, 2, 3)], [['lol', 'kek']]]

        for lst in uncorrect_input_lists:
            with self.assertRaises(AttributeError):
                list(gen(mock_file, lst))

    def test_empty_file(self):
        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['']
        lst = ['роза']

        result = list(gen(mock_file, lst))

        self.assertEqual(result, [])

    def test_is_Stop_Iter_after_gen_finished(self):
        lst = ['роза', 'проза']

        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['а Роза упала на лапу Азора',
                                           'разора азора ароза и роза зорара',
                                           'раз о розалин РОСАТОМ роз а',
                                           'ПРОЗА', 'рОзА']

        result = list(gen(mock_file, lst))

        # имитируем окончание итерации по генератору
        mock_file = MagicMock(spec=io.TextIOWrapper)

        with self.assertRaises(StopIteration):
            next(gen(mock_file, lst))

        self.assertEqual(result, ['а Роза упала на лапу Азора',
                                  'разора азора ароза и роза зорара',
                                  'ПРОЗА', 'рОзА'])

    def test_multiply_filters_in_line(self):

        lst = ['роза', 'азора']

        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['а Роза упала на лапу Азора',
                                           'разора азор а и зоро и зохан ароза и розаа зорара',
                                           'раз о розалин РОСАТОМ роз а',
                                           'РОЗАо и розамарин', 'рОзАы ароза', 'РОЗА и заноза с азора и роза по азора',
                                           'АЗОРА и ссора мимозы роза', 'азора роза азора роза азора']
        result = list(gen(mock_file, lst))

        self.assertEqual(result, ['а Роза упала на лапу Азора',
                                  'РОЗА и заноза с азора и роза по азора', 'АЗОРА и ссора мимозы роза',
                                  'азора роза азора роза азора'])

    def test_filter_is_full_equal_file_string(self):

        lst = ['роза', 'азора']

        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['РОЗА', 'АЗОРА', 'РОЗА\n',
                                           'азора\b\n', 'рОзА\t\n', 'азора',
                                           'розаазора', 'роз а', 'а зора']
        result = list(gen(mock_file, lst))

        self.assertEqual(result, ['РОЗА', 'АЗОРА', 'РОЗА',
                                  'рОзА', 'азора'])

    def test_filter_diff_registers(self):

        lst = ['роза', 'азора', 'не избежать позора']

        mock_file = MagicMock(spec=io.TextIOWrapper)
        mock_file.__iter__.return_value = ['А РОЗА УПАЛА НА ЛАПУ АЗОРА',
                                           'не всякий сумеет избежать позора',
                                           'азорава розашка',
                                           'АзОрА пока  РозА',
                                           'РОза это не мимоза',
                                           'не избежать позора']
        result = list(gen(mock_file, lst))

        self.assertEqual(result, ['А РОЗА УПАЛА НА ЛАПУ АЗОРА',
                                  'АзОрА пока  РозА',
                                  'РОза это не мимоза'])


if __name__ == '__main__':
    unittest.main()
