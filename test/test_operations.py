import pytest

from app.operations import Number, add, subtract, multiply, divide


def test_number_type_alias_contains_int_and_float():
    assert int in Number.__args__
    assert float in Number.__args__


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (-1, 1, 0),
        (2.5, 3.5, 6.0),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (5, 3, 2),
        (3, 5, -2),
        (5.5, 2.0, 3.5),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 6),
        (-2, 3, -6),
        (2.5, 4, 10.0),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (6, 3, 2.0),
        (5.5, 2, 2.75),
        (-9, 3, -3.0),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero!"):
        divide(5, 0)
