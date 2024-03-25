
from param_helper import param


def test_func(phone: str, password: str, action: list[str], channel=0):
    print(param(type=1))  # Additional parameters
    ...


test_func('11122223333', '123456', ['a'], 1)  # default usage
test_func('11122223333', '123456', ['a'], None)  # auto hide None
test_func(11122223333, '123456', 'a', '0')  # automatic type conversion based on the default type and the annotation (only for types which constructor available)
