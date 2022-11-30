from copy import deepcopy


class Iterable:

    def __init__(self):
        self.__data = []

    def __setitem__(self, key, value):
        if key < len(self.__data):
            self.__data[key] = value
        elif key == len(self.__data):
            self.__data.append(value)
        else:
            raise IndexError

    def __getitem__(self, item):
        return self.__data[item]

    def __delitem__(self, key):
        self.__data.remove(key)

    def __next__(self):
        if self.__iterator < len(self.__data) - 1:
            self.__iterator += 1
            return self.__data[self.__iterator]
        else:
            raise StopIteration

    def __iter__(self):
        self.__iterator = -1
        return self

    def __len__(self):
        return len(self.__data)

    def __eq__(self, other):
        return self.__data == other

    def append(self, value):
        self.__setitem__(len(self.__data), value)

    def remove(self, key):
        self.__delitem__(key)


def sort_data(data, function):
    """
    GNOME SORT
    - If you are at the start of the array then go to the right element (from arr[0] to arr[1])
    - If the current array element is larger or equal to the previous array element then go one step right
    - If the current array element is smaller than the previous array element then swap these two elements and go one step backwards
    - Repeat steps 2) and 3) till ‘i’ reaches the end of the array (i.e- ‘n-1’)
    - If the end of the array is reached then stop and the array is sorted
    """
    cpy = deepcopy(data)
    i = 0
    if len(cpy) < 2:
        return cpy
    while i < len(cpy):
        if i == 0:
            i += 1
        if not function(data[i], data[i - 1]):
            i += 1
        else:
            data[i], data[i - 1] = data[i - 1], data[i]
            i -= 1
    return cpy


def filter_data(data, function):
    new = []
    for x in data:
        if function(x):
            new.append(x)
    return new
