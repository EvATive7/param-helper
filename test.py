
from param_helper import param


def test_func(phone: str, password: str, channel=0):
    print(param(type=1))  # Additional parameters
    ...


test_func('11122223333', '123456', None)
test_func('11122223333', '123456', '1')  # Automatic type conversion based on the default type
test_func(11122223333, '123456', 0)  # Automatic type conversion based on the annotation
