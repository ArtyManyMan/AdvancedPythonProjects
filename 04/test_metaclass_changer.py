import unittest
from metaclass_changer import CustomClass


class TestCustomMeta(unittest.TestCase):
    def test_customClass(self):

        self.assertEqual(CustomClass.custom_x, 50)
        self.assertEqual(CustomClass.custom_line(CustomClass), 100)

        with self.assertRaises(AttributeError):
            CustomClass.x

        with self.assertRaises(AttributeError):
            CustomClass.line()

        self.assertEqual(CustomClass.__str__(CustomClass), "Custom_by_metaclass")

    def test_behavior_instanse_of_custom_class(self):
        inst = CustomClass()

        self.assertEqual(inst.custom_x, 50)

        self.assertEqual(inst.custom_val, 99)

        self.assertEqual(inst.custom_line(), 100)

        self.assertEqual(str(inst), "Custom_by_metaclass")

        with self.assertRaises(AttributeError):
            inst.x

        with self.assertRaises(AttributeError):
            inst.val

        with self.assertRaises(AttributeError):
            inst.line()

        with self.assertRaises(AttributeError):
            inst.yyy

        inst.dynamic = "added later"

        self.assertEqual(inst.custom_dynamic, "added later")

        with self.assertRaises(AttributeError):
            inst.dynamic

    def test_inst(self):

        inst = CustomClass('some test text')
        self.assertEqual(inst.custom_val, 'some test text')

        inst.custom_val = 'another test text'
        self.assertEqual(inst.custom_custom_val, 'another test text')

        with self.assertRaises(AttributeError):
            inst.custom_val

    def test_custom_function(self):
        inst = CustomClass()

        def dummy_func():
            return "I'm a dummy function"

        inst.dummy_func = dummy_func
        self.assertEqual(inst.custom_dummy_func(), "I'm a dummy function")

    def test_change_dynamic_attribute_value(self):
        inst = CustomClass()
        inst.dynamic = "added later"
        inst.dynamic = "updated"
        self.assertEqual(inst.custom_dynamic, "updated")

    def test_add_magic_methods_args(self):

        def __hash__(self):
            return 'CHECK'

        CustomClass.__hash__ = __hash__
        self.assertEqual(CustomClass.__hash__(CustomClass), 'CHECK')
        with self.assertRaises(AttributeError):
            CustomClass.custom___hash__()

        inst = CustomClass()
        def __hash__(self):
            return 'CHECK'

        inst.__hash__ = __hash__

        self.assertEqual(inst.__hash__(inst), 'CHECK')

        with self.assertRaises(AttributeError):
            inst.custom___hash__()

        __dict__ = {1: 111}

        inst.__dict__ = __dict__

        self.assertEqual(inst.__dict__, {1: 111})
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_line(), 100)

        with self.assertRaises(AttributeError):
            inst.custom___dict__()

        with self.assertRaises(AttributeError):
            x = inst.x

        with self.assertRaises(AttributeError):
            x = inst.line()

if __name__ == '__main__':
    unittest.main()
