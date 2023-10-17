class CustomMeta(type):
    def __new__(metacls, name, bases, dct, *args, **kwargs):
        signature = 'custom_'
        dct_copy = dct.copy()
        for key in dct_copy:
            if not (key.startswith('__') and key.endswith('__')):
                new_key = signature + key
                tmp = dct[key]
                del dct[key]
                dct[new_key] = tmp
        return super().__new__(metacls, name, bases, dct)

    def __setattr__(self, key, value):
        if key.startswith('custom_') and hasattr(self, key):
            delattr(self, key)
        self.__dict__[f'custom_{key}'] = value

    @classmethod
    def __prepare__(metacls, name, bases):
        return {'__setattr__': metacls.__setattr__}


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
