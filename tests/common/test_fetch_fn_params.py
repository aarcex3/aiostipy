import inspect
from typing import Optional

import msgspec
import pytest

from aiostipy.common.decorators.http.methods import fetch_fn_params


class MyStruct(msgspec.Struct):
    x: int
    y: str


def test_params_with_type_hints_and_defaults():
    def sample_fn(a: int, b: str = "default") -> None:
        pass

    expected_output = {"a": (int, None), "b": (str, "default")}
    result = fetch_fn_params(sample_fn)
    assert result == expected_output


def test_params_with_type_hints_no_defaults():
    def sample_fn(a: int, b: str) -> None:
        pass

    expected_output = {"a": (int, None), "b": (str, None)}
    result = fetch_fn_params(sample_fn)
    assert result == expected_output


def test_params_missing_type_hints():
    def sample_fn(a, b: str) -> None:
        pass

    with pytest.raises(
        ValueError, match=r"Parameter a of function .* has no type hint"
    ):
        fetch_fn_params(sample_fn)


def test_no_params():
    def sample_fn() -> None:
        pass

    expected_output = {}
    result = fetch_fn_params(sample_fn)
    assert result == expected_output


def test_class_method():
    class MyClass:
        def my_method(self, a: int, b: Optional[str] = None) -> None:
            pass

    expected_output = {"a": (int, None), "b": (Optional[str], None)}
    result = fetch_fn_params(MyClass.my_method)
    assert result == expected_output


def test_struct_as_param():

    def sample_fn(a: MyStruct) -> None:
        pass

    expected_output = {"a": (MyStruct, None)}
    result = fetch_fn_params(sample_fn)
    assert result == expected_output


def test_struct_as_param_with_default():

    def sample_fn(a: MyStruct = MyStruct(x=0, y="default")) -> None:
        pass

    expected_output = {"a": (MyStruct, MyStruct(x=0, y="default"))}
    result = fetch_fn_params(sample_fn)
    assert result == expected_output
