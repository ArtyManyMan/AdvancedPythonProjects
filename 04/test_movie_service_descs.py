import unittest
from movie_service_descs import MovieService


class TestMovieServiceDescriptors(unittest.TestCase):
    def test_name_desc(self):

        short_plot = """Stark, CEO of Stark Industries, was the chief weapons
manufacturer for the U.S. military. After a change of heart, he redirected his
technical knowledge into creating mechanized suits of armor for Earth's defense."""

        cast_dct = {'Robert Downey Jr.': 'Tony Stark',
                    'Terrence Howard': 'Rhodey',
                    'Jeff Bridges': 'Obadiah Stane',
                    'Gwyneth Paltrow': 'Pepper Potts'}

        service = MovieService('Iron Man', 7.4, short_plot, cast_dct)

        self.assertEqual(service.name_desc, 'Iron Man')

        with self.assertRaisesRegex(ValueError, 'Value should be of type str'):
            MovieService(4, 7.4, short_plot, cast_dct)

        with self.assertRaisesRegex(ValueError, 'Empty string'):
            MovieService('', 7.4, short_plot, cast_dct)

        with self.assertRaisesRegex(ValueError, 'Value should contain only English characters'):
            MovieService('Железный человек', 7.4, short_plot, cast_dct)

    def test_rate_desc(self):

        short_plot = """Stark, CEO of Stark Industries"""

        cast_dct = {'Robert Downey Jr.': 'Tony Stark',
                    'Terrence Howard': 'Rhodey',
                    'Jeff Bridges': 'Obadiah Stane',
                    'Gwyneth Paltrow': 'Pepper Potts'}

        name = 'Iron Man'

        service = MovieService(name, 7.4, short_plot, cast_dct)

        self.assertEqual(service.rate_desc, 7.4)

        with self.assertRaisesRegex(ValueError, 'Value should be of type int/float'):
            MovieService(name, '7.4', short_plot, cast_dct)

        with self.assertRaisesRegex(ValueError, 'Value should be greater or equal to 0'):
            MovieService(name, -1, short_plot, cast_dct)

    def test_plot_desc(self):

        short_plot_1 = """Stark, CEO of Stark Industries, was the chief weapons
manufacturer for the U.S. military. After a change of heart, he redirected his
technical knowledge into creating mechanized suits of armor for Earth's defense."""

        short_plot_2 = """Stark is initially depicted as an industrialist 
who is CEO of Stark Industries.
Initially the chief weapons manufacturer for the U.S. military, he has a change of heart
and redirects his technical knowledge into the creation of mechanized suits of armor
to defend Earth."""

        short_plot_3 = """Stark is initially depicted as an industrialist 
        who is CEO of Stark Industries.
        Initially the chief weapons manufacturer for the U.S. military, he has a change of heart
        and redirects his technical knowledge into the creation of mechanized suits of armor
        to defend Earth. Stark is initially depicted as an industrialist 
        who is CEO of Stark Industries.
        Initially the chief weapons manufacturer for the U.S. military, he has a change of heart
        and redirects his technical knowledge into the creation of mechanized suits of armor
        to defend Earth."""

        cast_dct = {'Robert Downey Jr.': 'Tony Stark',
                    'Terrence Howard': 'Rhodey',
                    'Jeff Bridges': 'Obadiah Stane',
                    'Gwyneth Paltrow': 'Pepper Potts'}

        name = 'Iron Man'

        service = MovieService(name, 7.4, short_plot_1, cast_dct)

        self.assertEqual(service.plot_desc, short_plot_1)

        with self.assertRaisesRegex(ValueError, 'Value should be of type str'):
            MovieService(name, 7.4, 789, cast_dct)

        with self.assertRaisesRegex(ValueError, 'Description should contain at most 250 characters'):
            MovieService(name, 7.4, short_plot_2, cast_dct)

        with self.assertRaisesRegex(ValueError, 'Description should contain at most 50 words'):
            MovieService(name, 7.4, short_plot_3, cast_dct)

    def test_cast_desc(self):

        short_plot = """Stark, CEO of Stark Industries"""

        cast_dct_1 = {'Robert Downey Jr.': 'Tony Stark',
                    'Terrence Howard': 'Rhodey',
                    'Jeff Bridges': 'Obadiah Stane',
                    'Gwyneth Paltrow': 'Pepper Potts'}

        cast_dct_2 = {"actor1": "name1", "actor2": "name2", "actor3": "name3",
                    "actor4": "name4", "actor5": "name5", "actor6": "name6",
                    "actor7": "name7", "actor8": "name8", "actor9": "name9",
                    "actor10": "name10", "actor11": "name11"}

        name = 'Iron Man'

        service = MovieService(name, 7.4, short_plot, cast_dct_1)

        self.assertEqual(service.cast_desc, cast_dct_1)

        with self.assertRaisesRegex(ValueError, 'Value should be of type dict'):
            MovieService(name, 7.4, short_plot, ['Robert Downey Jr.', 'Tony Stark'])

        with self.assertRaisesRegex(ValueError, 'The number of actors should not exceed 10'):
            MovieService(name, 7.4, short_plot, cast_dct_2)

    def test_get_full_info(self):

        short_plot = """Stark, CEO of Stark Industries, was the chief weapons
        manufacturer for the U.S. military. After a change of heart, he redirected his
        technical knowledge into creating mechanized suits of armor for Earth's defense."""

        cast_dct = {'Robert Downey Jr.': 'Tony Stark',
                    'Terrence Howard': 'Rhodey',
                    'Jeff Bridges': 'Obadiah Stane',
                    'Gwyneth Paltrow': 'Pepper Potts'}

        name = 'Iron Man'

        result = ('Name of Film: Iron Man', 'Rating: 7.4',
                  "Plot: Stark, CEO of Stark Industries, was the chief weapons\n        "
                  "manufacturer for the U.S. military. After a change of heart, he redirected his\n        "
                  "technical knowledge into creating mechanized suits of armor for Earth's defense.",
                  'Actors: Robert Downey Jr. Tony Stark',
                  'Terrence Howard Rhodey\nJeff Bridges Obadiah Stane\nGwyneth Paltrow Pepper Potts\n')

        service = MovieService(name, 7.4, short_plot, cast_dct)

        self.assertEqual(service.get_full_info(), result)

if __name__ == '__main__':
    unittest.main()


