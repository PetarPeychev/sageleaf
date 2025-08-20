#!/bin/bash

uv run pytest -vv
uv run pyright
uv run ruff format
uv run ruff check --fix