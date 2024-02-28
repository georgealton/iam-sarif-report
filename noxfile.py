import nox
from nox.sessions import Session

BASE_PYTHON = "3.12"
ALL_PYTHON_VERSIONS = ("3.8", "3.9", "3.10", "3.11", "3.12")


@nox.session(python=ALL_PYTHON_VERSIONS, tags=["tests"])
def test(session: Session) -> None:
    """Run Tests."""
    session.install(".[test]")
    session.run("pytest", "-v")


@nox.session(python=BASE_PYTHON, tags=["lint"])
def pre_commit(session: Session) -> None:
    """Run pre-commit."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")
