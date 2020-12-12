from __future__ import annotations

from typing import Any, Optional

from _pytest.mark.structures import MarkDecorator

import pytest


class Case:
    def __init__(self, label: Optional[str] = None, /, **kwargs: Any):
        self.label = label
        self.kwargs = kwargs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Case):
            return False

        return (self.label == other.label) and (self.kwargs == other.kwargs)

    def __repr__(self) -> str:
        pairs = [f"{key}={value!r}," for key, value in self.kwargs.items()]
        joined = " ".join(pairs)
        label = f"'{self.label}', " if self.label is not None else ""
        return f"Case({label}{joined})"


def parametrize_cases(*cases: Case) -> MarkDecorator:
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
