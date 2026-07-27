FROM python:3.12-slim

# Avoid .pyc files and buffer stdout/stderr so logs stream immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /src

# Copy build inputs, install project + deps
COPY pyproject.toml README.md ./
COPY ./src /src
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e ".[dev]"

# Make entrypoint script(s) executable
COPY ./scripts/ /scripts/
RUN chmod -R +x /scripts

# Unprivileged user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /src

USER app

CMD ["/scripts/start.sh"]
