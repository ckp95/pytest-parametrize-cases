# pytest-parametrize-cases

[![Tests](https://github.com/ckp95/pytest-parametrize-cases/workflows/Tests/badge.svg)](https://github.com/ckp95/pytest-parametrize-cases/actions?workflow=Tests)

## What is it?

The way [parametrized tests](https://docs.pytest.org/en/stable/parametrize.html) work in `pytest` annoys me:

```python
import pytest


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expecteds
```

Passing in argument names as a comma-separated string just looks ugly and un-Pythonic, and you have to give each case as an anonymous tuple and make sure to get the order right every time. This becomes harder the more parameters you have. It's also a bit awkward to specify the test IDs. Even when you use `pytest.param` there's still nothing stopping you from getting the order of the parameters wrong.

So, I wrote a simple wrapper around `pytest.mark.parametrize` which makes it a bit nicer to read and use. The previous example would be written:

```python
from pytest_parametrize_cases import Case, parametrize_cases


@parametrize_cases(
    Case(test_input="3+5", expected=8),
    Case(test_input="2+4", expected=6),
    Case(test_input="6*9", expected=42)
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

It also supports optional test IDs. Using the [same example as the one in the pytest docs](https://docs.pytest.org/en/stable/example/parametrize.html#different-options-for-test-ids) for `pytest.mark.parametrize`, this is how you include them:


```python
from datetime import datetime, timedelta

from pytest_parametrize_cases import Case, parametrize_cases

@parametrize_cases(
    Case(
        "forward",
        a=datetime(2001, 12, 12),
        b=datetime(2001, 12, 11),
        expected=timedelta(1),
    ),
    Case(
        "backward",
        a=datetime(2001, 12, 11),
        b=datetime(2001, 12, 12),
        expected=timedelta(-1),
    ),
)
def test_timedistance_v4(a, b, expected):
    diff = a - b
    assert diff == expected
```

That is to say, you decorate your test function with `@parametrize_cases` and pass in multiple instances of `Case` as arguments. The arguments to the `Case` constructor are [optionally] a positional-only string which constitutes the test ID (printed when you use the `-v / --verbose` flag), and then keyword arguments for each of the parameters the test function expects.

In my opinion this is much more readable and user-friendly than the default way of writing parametrized tests. Related data is kept together rather than spread out in multiple containers. Specifying the keyword arguments is mandatory, so it is always clear where each piece of data ends up in the test function (explicit is better than implicit). And it is more convenient to specify test IDs.

The `parametrize_cases` decorator can be stacked multiple times to give the Cartesian product of your parametrizations, in the exact same way as `mark.parametrize`.

## Dependencies

- Python >= 3.8
- `pytest`

## Installation

```
pip install pytest-parametrize-cases
```

Or just look in `src/pytest_parametrize_cases/case.py` and copypaste the two definitions to somewhere in your test suite.
