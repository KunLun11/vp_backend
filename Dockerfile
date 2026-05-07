FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --all-groups

COPY . /app

RUN uv sync --frozen --all-groups

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]