# pytest-parametrize-cases

Simple wrapper around `pytest.mark.parametrize` which makes it more user-friendly. Just paste this somewhere in your test suite (`conftest.py` is a good idea) then import `Case` and `parametrize_cases`.

```python
class Case:
    def __init__(self, label: Optional[str] = None, /, **kwargs):
        self.label = label
        self.kwargs = kwargs

    def __repr__(self):
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
