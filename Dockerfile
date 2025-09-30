FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
RUN mkdir -p /work
COPY ./pyproject.toml /work
COPY ./uv.lock /work
COPY ./app /work/app
COPY ./.env.prod /work/.env

# Install the application dependencies.
WORKDIR /work
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/work/.venv/bin/fastapi", "run", "app/main.py", "--port", "8001", "--host", "0.0.0.0"]
