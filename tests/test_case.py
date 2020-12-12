import pytest

from pytest_parametrize_cases import Case, parametrize_cases


def test_case_eq():
    case_1 = Case("foo", bar=10, baz=...)
    case_2 = Case(bar=10, baz=...)
    case_3 = Case("foo", bar=11, baz=...)

    assert case_1 == case_1
    assert case_1 != case_2
    assert case_2 != case_3
    assert case_1 != case_3
    assert case_1 != 10


def test_case_repr():
    case = Case("foo", bar=10, baz=...)
    assert repr(case) == "Case('foo', bar=10, baz=Ellipsis,)"
    assert eval(repr(case)) == case

    case = Case(var1="something", var2="something else")
    assert repr(case) == "Case(var1='something', var2='something else',)"
    assert eval(repr(case)) == case


def test_one_case():
    standard = pytest.mark.parametrize(argnames="foo,bar", argvalues=[(3, "something")])
    wrapped = parametrize_cases(Case(foo=3, bar="something"))

    assert wrapped == standard


def test_multiple_cases():
    standard = pytest.mark.parametrize(
        argnames="foo,bar",
        argvalues=[(3, "something"), (None, -100), ([10, 20, 30], ...)],
    )
    wrapped = parametrize_cases(
        Case(foo=3, bar="something"),
        Case(foo=None, bar=-100),
        Case(foo=[10, 20, 30], bar=...),
    )

    assert wrapped == standard


def test_one_argument():
    standard = pytest.mark.parametrize(
        argnames="bar",
        argvalues=[3, -100, ...],
    )
    wrapped = parametrize_cases(Case(bar=3), Case(bar=-100), Case(bar=...))

    assert wrapped == standard


def test_ids():
    standard = pytest.mark.parametrize(
        argnames="foo,bar",
        argvalues=[(3, "something"), (None, -100), ([10, 20, 30], ...)],
        ids=["thing_1", None, "thing_3"],
    )
    wrapped = parametrize_cases(
        Case("thing_1", foo=3, bar="something"),
        Case(foo=None, bar=-100),
        Case("thing_3", foo=[10, 20, 30], bar=...),
    )

    assert wrapped == standard


def test_arg_reorder():
    standard = pytest.mark.parametrize(
        argnames="foo,bar,baz",
        argvalues=[
            (3, "something", 777),
            (None, -100, "aaaaa"),
            ([10, 20, 30], ..., 0),
        ],
    )
    wrapped = parametrize_cases(
        Case(foo=3, bar="something", baz=777),
        Case(bar=-100, baz="aaaaa", foo=None),
        Case(baz=0, bar=..., foo=[10, 20, 30]),
    )

    assert wrapped == standard


def test_inconsistent_parameters():
    with pytest.raises(ValueError) as e:
        parametrize_cases(Case(foo=10, bar=20), Case(foo=10, baz=30))

    assert e.match(
        r"Inconsistent parametrization: "
        r"Case\(foo=10, bar=20,\), Case\(foo=10, baz=30,\)"
    )
