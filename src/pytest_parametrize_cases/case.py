"""Case class and parametrize_cases function."""


from __future__ import annotations

from typing import Any, Optional

from _pytest.mark.structures import MarkDecorator

import pytest


class Case:
    """Container for a test case, with optional test ID.

    Attributes:
        label: Test ID. Will be displayed for each test when running `pytest -v`
            This is positional-only, and optional.
        kwargs: Parameters used for the test cases.

    Example:
        Case("some test name", foo=10, bar="some value")
        Case(foo=99, bar="some other value") # no name given
    """

    def __init__(self, label: Optional[str] = None, /, **kwargs: Any):
        """Initializes Case class with label (optional) and kwargs."""
        self.label = label
        self.kwargs = kwargs

    def __eq__(self, other: object) -> bool:
        """Return self==value."""
        if not isinstance(other, Case):
            return False

        return (self.label == other.label) and (self.kwargs == other.kwargs)

    def __repr__(self) -> str:
        """Return repr(self)."""
        pairs = [f"{key}={value!r}," for key, value in self.kwargs.items()]
        joined = " ".join(pairs)
        label = f"'{self.label}', " if self.label is not None else ""
        return f"Case({label}{joined})"


def parametrize_cases(*cases: Case) -> MarkDecorator:
    """Decorator wrapper for pytest.mark.parametrize.

    Args:
        *cases:
            One or more Case objects. They must all have the same set of named
            keyword arguments.

    Returns:
        A suitable MarkDecorator instance.

    Example:
        from datetime import datetime, timedelta

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
        def test_timedistance(a, b, expected):
            diff = a - b
            assert diff == expected
    """
    first_case = cases[0]
    first_args = first_case.kwargs.keys()

    for case in cases:
        if first_args != case.kwargs.keys():
            msg = f"Inconsistent parametrization: {first_case!r}, {case!r}"
            raise ValueError(msg)

    argnames = ",".join(first_args)

    argvalues = [tuple(case.kwargs[i] for i in first_args) for case in cases]
    if len(first_args) == 1:
        argvalues = [i[0] for i in argvalues]

    ids = [case.label for case in cases]
    if all(i is None for i in ids):
        return pytest.mark.parametrize(argnames=argnames, argvalues=argvalues)

    return pytest.mark.parametrize(argnames=argnames, argvalues=argvalues, ids=ids)
