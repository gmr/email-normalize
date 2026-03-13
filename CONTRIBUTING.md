# Contributing

To get setup in the environment and run the tests, take the following steps:

```bash
uv sync --all-extras
uv run pre-commit install

uv run pre-commit run --all-files
uv run coverage run && uv run coverage report
```

## Adding a Mailbox Provider

If you know the features for a mailbox provider, simply modify
`email_normalize.providers` adding a new class for the provider.
Set the flags in the new class appropriately and add tests.

## Test Coverage

Pull requests that make changes or additions that are not covered by tests
will likely be closed without review.

In addition, all tests must pass the tests **AND** ruff linter. If ruff
exceptions are included, the reasoning for adding the exception must be included
in the pull request.
