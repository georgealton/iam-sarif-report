import nox
from nox.sessions import Session

BASE_PYTHON = "3.11"
ALL_PYTHON_VERSIONS = ("3.7", "3.8", "3.9", "3.10", "3.11")


@nox.session(python=ALL_PYTHON_VERSIONS)
def test(session: Session) -> None:
    session.install(".[test]")
    session.run("pytest", "-v")


@nox.session(python=BASE_PYTHON)
def pre_commit(session: Session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
