class A():
    pass

def __hash__(self):
    return 'KEK'

print(A.__hash__('lol'))
print(A.__hash__('lol'))
a = A()
print(a.__hash__())