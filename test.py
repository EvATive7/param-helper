
from param_helper import param


def test_func(phone: str, password: str, action: list[str], channel=0):
    origin_vars = locals().copy()
    param_vars = param(type=1)  # Additional parameters

    print(
f"""
{origin_vars}
->
{param_vars}
"""
)

    # You can view vars in debugging
    ...


test_func('11122223333', '123456', ['a'], 1)  # default usage
test_func('11122223333', '123456', ['a'], None)  # Automatically hide fields with a value of None
test_func(11122223333, '123456', 'a', '0')  # Automatic type conversion based on default value and annotation (only for types where constructors are available)
