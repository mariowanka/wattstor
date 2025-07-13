FROM python:3.12-slim

RUN pip install poetry==1.8.2

ENV APP_HOME="/wattstor/app"
WORKDIR $APP_HOME

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
RUN poetry install --without test --no-root

COPY . $APP_HOME

RUN pip install gunicorn

EXPOSE 8000

# CMD ["python3", "app.py"]
CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]