from invoke import Context, task

# Invoke doesn't support type annotations, it looks like
# so I had to use comments


@task
def start(c):
    # type: (Context) -> None
    c.run("poetry run python3 main.py")


@task
def format(c):
    # type: (Context) -> None
    c.run("poetry run black .")
    c.run("poetry run isort .")


@task
def lint(c):
    # type: (Context) -> None
    c.run("poetry run flake8 .")
    c.run("poetry run mypy .")
