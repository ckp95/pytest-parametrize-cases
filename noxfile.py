import tempfile
from pathlib import Path

import nox

locations = ["src", "tests", "noxfile.py"]


@nox.session(python=["3.8", "3.9"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session(python=["3.8", "3.9"])
def mypy(session):
    args = session.posargs or ["src"]
    session.run("poetry", "install", external=True)
    session.run("mypy", "--strict", *args)


@nox.session(python=["3.8", "3.9"])
def py_typed(session):
    # have to pip install to make sure not in editable mode, see
    # https://github.com/python-poetry/poetry/issues/1382
    session.run("pip", "install", "-q", ".", "mypy")

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


@nox.session(python=["3.8", "3.9"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-import-order", "flake8-bugbear")
    session.run("flake8", *args)
