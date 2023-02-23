import nox

base_python = "python3.11"

python_versions = [
    "python3.7",
    "python3.8",
    "python3.9",
    "python3.10",
    "python3.11",
]

@nox.session(python=python_versions)
def test(session):
    session.install(".[test]")
    session.run("pytest", "-v")

@nox.session(python=base_python)
def pre_commit(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")

