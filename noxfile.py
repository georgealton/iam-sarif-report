import nox

base_python = "3.11"

python_versions = [
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
]

@nox.session(python=python_versions)
def test(session):
    session.install(".[test]")
    session.run("pytest", "-v")

@nox.session(python=base_python)
def pre_commit(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")

