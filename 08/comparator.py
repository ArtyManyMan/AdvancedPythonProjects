import timeit
import weakref


class MyClass:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class MySlottedClass:
    __slots__ = ['a', 'b', 'c']
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class MyWeakRefClass:
    def __init__(self, a, b, c):
        self.a = weakref.ref(a) if not isinstance(a, int) else a
        self.b = weakref.ref(b) if not isinstance(b, int) else b
        self.c = weakref.ref(c) if not isinstance(c, int) else c

def measure_instance_creation(class_type, num_instances):
    stmt = f"{class_type.__name__}(1, 2, 3)"
    setup = f"from __main__ import {class_type.__name__}"
    creation_time = timeit.timeit(stmt, setup=setup, number=num_instances)
    return creation_time

def measure_attribute_access(class_instances, num_iterations):
    read_time = timeit.timeit(lambda: [obj.a for obj in class_instances], number=num_iterations)
    write_time = timeit.timeit(lambda: [setattr(obj, 'a', 5) for obj in class_instances], number=num_iterations)
    return read_time, write_time

def main_func():
    num_instances = 100000

    creation_time_normal = measure_instance_creation(MyClass, num_instances)
    creation_time_slotted = measure_instance_creation(MySlottedClass, num_instances)
    creation_time_weakref = measure_instance_creation(MyWeakRefClass, num_instances)

    print("Время создания экземпляров:")
    print(f"Обычные атрибуты: {creation_time_normal}")
    print(f"Слоты: {creation_time_slotted}")
    print(f"Атрибуты weakref: {creation_time_weakref}")

    instances_normal = [MyClass(1, 2, 3) for _ in range(num_instances)]
    instances_slotted = [MySlottedClass(1, 2, 3) for _ in range(num_instances)]
    instances_weakref = [MyWeakRefClass(1, 2, 3) for _ in range(num_instances)]

    num_iterations = 1000

    read_time_normal, write_time_normal = measure_attribute_access(instances_normal, num_iterations)
    read_time_slotted, write_time_slotted = measure_attribute_access(instances_slotted, num_iterations)
    read_time_weakref, write_time_weakref = measure_attribute_access(instances_weakref, num_iterations)

    print("\nВремя чтения атрибутов:")
    print(f"Обычные атрибуты: {read_time_normal}")
    print(f"Слоты: {read_time_slotted}")
    print(f"Атрибуты weakref: {read_time_weakref}")

    print("\nВремя записи атрибутов:")
    print(f"Обычные атрибуты: {write_time_normal}")
    print(f"Слоты: {write_time_slotted}")
    print(f"Атрибуты weakref: {write_time_weakref}")



