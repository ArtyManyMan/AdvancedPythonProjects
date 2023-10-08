"""
This module contains unit tests for the 'predict_message_mood'
function in the 'home_work_ex1' module.
"""

import unittest
from unittest import mock
from predicator import predict_message_mood, SomeModel


class TestPredictMessageMood(unittest.TestCase):

    def test_predict_message_mood_norm(self):
        mock_model = mock.Mock(spec=SomeModel)

        predict_values = [0.4, 0.55, 0.7]

        for predict_value in predict_values:
            mock_model.predict.return_value = predict_value
            result = predict_message_mood("Средняя окраска", mock_model)
            self.assertEqual(result, 'норм')

    def test_predict_message_mood_bad(self):
        mock_model = mock.Mock(spec=SomeModel)

        predict_values = [0.2, 0.1, 0.05]

        for predict_value in predict_values:
            mock_model.predict.return_value = predict_value
            result = predict_message_mood("Вулкан", mock_model)
            self.assertEqual(result, 'неуд')

    def test_predict_message_mood_good(self):
        mock_model = mock.Mock(spec=SomeModel)

        predict_values = [0.85, 0.9, 0.95]

        for predict_value in predict_values:
            mock_model.predict.return_value = predict_value
            result = predict_message_mood("Чапаев и пустота", mock_model)
            self.assertEqual(result, 'отл')

    def test_predict_message_mood_edge_cases(self):
        mock_model = mock.Mock(spec=SomeModel)

        edge_cases = [
            ("Порог 'неуд'", 0.29, 'неуд'),
            ("Порог 'норм'", 0.3, 'норм'),
            ("Порог 'норм'", 0.8, 'норм'),
            ("Порог 'отл'", 0.81, 'отл'),
        ]

        for message, predict_value, expected_result in edge_cases:
            mock_model.predict.return_value = predict_value
            result = predict_message_mood(message, mock_model)
            self.assertEqual(result, expected_result)

    def test_predict_message_mood_invalid_input(self):
        mock_model = mock.Mock(spec=SomeModel)

        invalid_inputs = [None, 123, 0.5, True, SomeModel()]

        for i in invalid_inputs:
            with self.assertRaises(TypeError):
                predict_message_mood(i, mock_model)

    def test_predict_message_mood_invalid_model(self):
        invalid_models = [None, 123, "Not a SomeModel instance", True]

        for model in invalid_models:
            with self.assertRaises(TypeError) as context:
                predict_message_mood("Сообщение", model)

            # Проверяем, содержит ли сообщение исключения ожидаемую строку
            expected_message = 'Do not belong class SomeModel'
            self.assertEqual(str(context.exception), expected_message)

    def test_predict_message_mood_invalid_result(self):
        mock_model = mock.Mock(spec=SomeModel)

        invalid_results = [None, "Not a float", 123, True]

        for result in invalid_results:
            mock_model.predict.return_value = result

            with self.assertRaises(TypeError) as context:
                predict_message_mood("Сообщение", mock_model)

            expected_message = 'Not float'
            self.assertEqual(str(context.exception), expected_message)

    def test_predict_calls_check_expected_calls(self):

        mock_model = mock.Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.1

        predict_message_mood('Вулкан', mock_model)
        predict_message_mood('Ураган', mock_model)

        # cоздаем список ожидаемых вызовов метода predict
        expected_calls = [mock.call('Вулкан'), mock.call('Ураган')]

        # проверяем вызов метода predict с ожидаемыми аргументами
        mock_model.predict.assert_has_calls(expected_calls)

    def test_threshold_changes(self):
        mock_model = mock.Mock(spec=SomeModel)
        mock_model.predict.return_value = 0.7

        with self.assertRaises(ValueError) as msg:
            predict_message_mood('ТЕКСТ-ТЕКСТ', mock_model, 0.99, 0.01)
        self.assertEqual("bad_thresholds can't be higher or equal good_thresholds", msg.exception.args[0])

        with self.assertRaises(ValueError) as msg:
            predict_message_mood('какой-то текст', mock_model, 0.7, 0.7)
        self.assertEqual("bad_thresholds can't be higher or equal good_thresholds", msg.exception.args[0])

        with self.assertRaises(ValueError) as msg:
            predict_message_mood('ещё текст', mock_model, 0.11, 0.11)
        self.assertEqual("bad_thresholds can't be higher or equal good_thresholds", msg.exception.args[0])

        with self.assertRaises(ValueError):
            predict_message_mood('ещё текст', mock_model, 1, 0)
        self.assertEqual("bad_thresholds can't be higher or equal good_thresholds", msg.exception.args[0])

        mock_model.predict.side_effect = [0.22, 0.11, 0.3, 1.0, 0.74, 0.0, 1.0]

        expected_calls = [mock.call('Пурпурная вода'),
                          mock.call('Лесная ягода'),
                          mock.call('Золотая орда'),
                          mock.call('Защитник рода'),
                          mock.call('закрыть/открыть ворота'),
                          mock.call('термальная погода'),
                          mock.call('Кольцо принёс? Фродо!')
                          ]

        self.assertEqual('отл', predict_message_mood('Пурпурная вода', mock_model, 0.1, 0.2))
        self.assertEqual('норм', predict_message_mood('Лесная ягода', mock_model, 0.11, 0.12))
        self.assertEqual('неуд', predict_message_mood('Золотая орда', mock_model, 0.5, 0.55))
        self.assertEqual('отл', predict_message_mood('Защитник рода', mock_model, 0.01, 0.99))
        self.assertEqual('норм', predict_message_mood('закрыть/открыть ворота', mock_model, 0.70, 0.75))
        self.assertEqual('неуд', predict_message_mood('термальная погода', mock_model, 0.4, 0.404))
        self.assertEqual('норм', predict_message_mood('Кольцо принёс? Фродо!', mock_model, 0.0, 1.0))

        self.assertEqual(expected_calls, mock_model.predict.mock_calls)


if __name__ == '__main__':
    unittest.main()
