import tempfile
from pathlib import Path

import nox

locations = ["src", "tests"]


@nox.session(python=["3.8", "3.9", "3.10"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session(python=["3.8", "3.9", "3.10"])
def mypy(session):
    args = session.posargs or ["src"]
    session.run("poetry", "install", external=True)
    session.run("mypy", "--strict", *args)


@nox.session(python=["3.10"])
def py_typed(session):
    # have to pip install to make sure not in editable mode, see
    # https://github.com/python-poetry/poetry/issues/1382
    session.install(".", "mypy")

    # if we haven't included py.typed in the package, mypy --strict should
    # complain about missing imports. if we have included it, mypy is happy.
    script = "from pytest_parametrize_cases import Case, parametrize_cases"
    # script = "def foo() -> int: return 5"

    with tempfile.TemporaryDirectory() as temp_dir:
        filename = "foo.py"
        filepath = Path(temp_dir) / filename
        with open(filepath, "w") as f:
            print(script, file=f)

        session.run("mypy", "--strict", str(filepath))


@nox.session(python=["3.10"])
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-import-order",
        "flake8-bugbear",
        "flake8-docstrings",
    )
    session.run("flake8", *args)
