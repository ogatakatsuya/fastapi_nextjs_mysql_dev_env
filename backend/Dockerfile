FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml* poetry.lock* ./

RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000", "--reload"]