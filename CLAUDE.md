# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`email-normalize` is a Python 3.11+ library that normalizes email addresses by stripping mailbox-provider-specific behaviors (plus addressing, period stripping, etc.). It uses async DNS (aiodns) to resolve MX records and match them against known providers, with a synchronous wrapper for non-async callers.

## Commands

```bash
# Install dependencies (uses uv)
uv sync --all-extras

# Run tests
uv run coverage run
uv run coverage report

# Run a single test
uv run python -m unittest tests.test_normalize.MailboxProviderTestCase.test_google

# Lint (ruff format + ruff check via pre-commit)
uv run pre-commit run --all-files
```

## Architecture

Two-module library under `email_normalize/`:

- **`__init__.py`** — Core logic: `Normalizer` (async class with LFRU-cached MX lookups), `Result` dataclass, and `normalize()` sync wrapper. The `Normalizer` resolves MX records, matches them to providers, then applies provider-specific normalization rules. `skip_dns=True` mode bypasses MX lookups and uses a static `DomainMap` instead.

- **`providers.py`** — Provider definitions: `Rules` flag enum (`PLUS_ADDRESSING`, `STRIP_PERIODS`, `LOCAL_PART_AS_HOSTNAME`), `MailboxProvider` base class, concrete provider classes (Apple, Fastmail, Google, etc.), `Providers` list (for MX matching), and `DomainMap` dict (for skip_dns mode).

## Code Style

- Ruff with 79-char line length, single quotes
- See `pyproject.toml` `[tool.ruff.lint]` for the full rule selection
