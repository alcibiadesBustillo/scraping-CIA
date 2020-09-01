"""
It is just for practice iterators
"""

my_list = [1, 2, 3, 4, 5, 6]
my_iter = iter(my_list)

print(type(my_iter))

# Extract the elements
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))

