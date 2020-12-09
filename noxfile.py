import nox

locations = ["src", "tests", "noxfile.py"]


@nox.session(python=["3.8", "3.9"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session(python=["3.8", "3.9"])
def lint(session):
    args = session.posargs or locations
    session.install("black")
    session.install("flake8")
    session.run("black", *args)
    session.run("flake8", *args)
