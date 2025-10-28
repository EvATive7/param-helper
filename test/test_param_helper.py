import param_helper as ph


def mod_foo_basic(a, b):
    return ph.param()


def mod_foo_cast(a: int, b="y", c=None, d: float = 1.2, e=10):
    # a: annotated -> cast to int
    # b: no annotation, default present -> cast using type(default) i.e. str
    # c: value None -> skipped
    # d: annotated float -> cast
    # e: no annotation, default present -> cast using type(default) i.e. int
    return ph.param()


def mod_foo_unannotated(x):
    return ph.param()


class Greeter:
    def greet(self, name: str):
        return ph.param()


def mod_foo_kwargs(a: int, b: str = "x"):
    # Provide an override via kwargs and add new key
    return ph.param(b="y", extra=1)


def mod_foo_multi(a, tags):
    return ph.param(prmhlpr_multi_key_mode_=True)


def test_function_basic_no_annotations():
    out = mod_foo_basic(1, "x")
    assert out == {"a": 1, "b": "x"}


def test_casting_with_annotations_and_default_type():
    out = mod_foo_cast("5", 7, None, "3.14", "42")
    assert out["a"] == 5 and isinstance(out["a"], int)
    assert out["b"] == "7" and isinstance(out["b"], str)
    assert "c" not in out
    assert abs(out["d"] - 3.14) < 1e-9 and isinstance(out["d"], float)
    assert out["e"] == 42 and isinstance(out["e"], int)


def test_unannotated_without_default_keeps_type():
    out = mod_foo_unannotated("3")
    assert out["x"] == "3"


def test_method_support():
    g = Greeter()
    out = g.greet(123)
    assert out == {"name": "123"}


def test_kwargs_merge_and_override():
    out = mod_foo_kwargs("5", b=0)
    # a casts to int, b overridden to "y", and extra present
    assert out == {"a": 5, "b": "y", "extra": 1}


def test_multi_key_mode_list_and_tuple_expand():
    out = mod_foo_multi(1, tags=["x", "y"])
    assert sorted(out) == sorted([("a", 1), ("tags", "x"), ("tags", "y")])

    out2 = mod_foo_multi(2, tags=("m", "n"))
    assert sorted(out2) == sorted([("a", 2), ("tags", "m"), ("tags", "n")])
