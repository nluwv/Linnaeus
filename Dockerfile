FROM python:3.12-slim-bookworm

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VERSION=2.0.1


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR /app

COPY . .

# Install project dependencies globally using Poetry
RUN pip install poetry==$POETRY_VERSION

RUN poetry lock

RUN poetry install


# Set up for use in VS Code dev containers
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*