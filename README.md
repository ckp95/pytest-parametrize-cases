# pytest-parametrize-cases

The way parametrized tests work in `pytest` annoyed the hell out of me (seriously, passing in argument names as a comma separated string???), so I wrote a simple wrapper around `pytest.mark.parametrize` which makes it more user-friendly. Just paste this somewhere in your test suite (`conftest.py` is a good idea) then import `Case` and `parametrize_cases`. This is not an installable package (yet).

```python
class Case:
    def __init__(self, label: Optional[str] = None, /, **kwargs):
        self.label = label
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"Case({self.label!r}, **{self.kwargs!r})"


def parametrize_cases(*cases: Case):
    for case in cases:
        if not isinstance(case, Case):
            raise TypeError(f"{case!r} is not an instance of Case")

    first_case = cases[0]
    first_args = first_case.kwargs.keys()
    argument_string = ",".join(sorted(first_args))

    case_list = []
    ids_list = []
    for case in cases:
        args = case.kwargs.keys()

        if args != first_args:
            raise ValueError(
                f"Inconsistent signature: {first_case!r}, {case!r}"
            )

        case_tuple = tuple(value for key, value in sorted(case.kwargs.items()))
        case_list.append(case_tuple)
        ids_list.append(case.label)

    if len(first_args) == 1:
        # otherwise it gets passed to the test function as a singleton tuple
        case_list = [i[0] for i in case_list]

    return pytest.mark.parametrize(
        argnames=argument_string, argvalues=case_list, ids=ids_list
    )
```

Using the [same example as the one in the pytest docs](https://docs.pytest.org/en/stable/example/parametrize.html#different-options-for-test-ids) for `pytest.mark.parametrize`, this is how it is used:

```python
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

This is much more readable and user-friendly than the default way of writing parametrized tests. Related data is kept together rather than spread out in multiple containers. Specifying the keyword arguments is mandatory, so it is always clear where each piece of data ends up in the test function (explicit is better than implicit). And it is more convenient to specify test IDs.
