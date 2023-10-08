"""
This is a module that provides utility functions for working with strings.
"""


from random import random


class SomeModel:
    def predict(self, message: str) -> float:
        return round(random(), 2)


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    """ Predict the mood of a message based on a model's prediction. """

    if not isinstance(model, SomeModel):
        raise TypeError('Do not belong class SomeModel')

    if bad_thresholds >= good_thresholds:
        raise ValueError("bad_thresholds can't be higher or equal good_thresholds")

    result_predict = model.predict(message)

    if not isinstance(result_predict, float):
        raise TypeError('Not float')

    if result_predict < bad_thresholds:
        return 'неуд'
    elif result_predict > good_thresholds:
        return 'отл'
    else:
        return 'норм'


if __name__ == '__main__':
    model = SomeModel()
