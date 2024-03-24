FROM python:3.12-slim

RUN python -m pip install --upgrade poetry

WORKDIR /usr/src/app

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

COPY . .

CMD [ "poetry", "run", "python", "./import-uffd-users.py" ]
