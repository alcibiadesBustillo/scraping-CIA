def my_func():
    a = 1
    yield a

    a = 2
    yield a

    a = 3
    yield a


my_first_gen = my_func()

print(next(my_first_gen))
print(next(my_first_gen))
print(next(my_first_gen))

a = list((yield i) for i in range(3))
print(a)