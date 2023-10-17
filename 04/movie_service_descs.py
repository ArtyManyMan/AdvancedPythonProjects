class MovieName:
    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if instance is None:
            raise ValueError("You can't set value for None instance")

        if not isinstance(value, str):
            raise ValueError('Value should be of type str')

        if not value:
            raise ValueError('Empty string')

        for char in value:
            if char.isalpha() and char.lower() not in 'abcdefghijklmnopqrstuvwxyz ':
                raise ValueError('Value should contain only English characters')

        setattr(instance, self.name, value)

    def __delete__(self, instance):
        delattr(instance, self.name)


class RatingDescr:
    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if instance is None:
            raise ValueError("You can't set value for None instance")

        if not isinstance(value, (int, float)):
            raise ValueError('Value should be of type int/float')

        if value < 0:
            raise ValueError('Value should be greater or equal to 0')

        setattr(instance, self.name, value)

    def __delete__(self, instance):
        delattr(instance, self.name)


class MoviePlotDescr:
    max_words = 50
    max_characters = 250

    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if instance is None:
            raise ValueError("You can't set value for None instance")

        if not isinstance(value, str):
            raise ValueError('Value should be of type str')

        if len(value.split()) > self.max_words:
            raise ValueError(f'Description should contain at most {self.max_words} words')

        if len(value) > self.max_characters:
            raise ValueError(f'Description should contain at most {self.max_characters} characters')

        setattr(instance, self.name, value)

    def __delete__(self, instance):
        delattr(instance, self.name)


class MovieCastDescr:
    max_actors = 10

    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if instance is None:
            raise ValueError("You can't set value for None instance")

        if not isinstance(value, dict):
            raise ValueError('Value should be of type dict')

        if len(value) > self.max_actors:
            raise ValueError(f'The number of actors should not exceed {self.max_actors}')

        setattr(instance, self.name, value)

    def __delete__(self, instance):
        delattr(instance, self.name)


class MovieService:
    name_desc = MovieName()
    rate_desc = RatingDescr()
    plot_desc = MoviePlotDescr()
    cast_desc = MovieCastDescr()

    def __init__(self, name, rate, plot, cast):
        self.name_desc = name
        self.rate_desc = rate
        self.plot_desc = plot
        self.cast_desc = cast

    def get_full_info(self):
        res1 = "Name of Film: " + self.name_desc
        res2 = "Rating: " + str(self.rate_desc)
        res3 = "Plot: " + self.plot_desc
        res4 = "Actors: "
        res5 = ''
        for pos, k_v in enumerate(self.cast_desc.items()):
            if pos < 1:
                res4 += ' '.join(map(str, k_v))
                continue
            res5 += ' '.join(map(str, k_v)) + '\n'
        return (res1, res2, res3, res4, res5)
