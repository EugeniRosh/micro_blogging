FROM python:3.10 as requirements_stage

ENV PYTHONUNBUFFERED=1

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without -hashes

FROM python:3.10

WORKDIR /project

COPY --from=requirements_stage /tmp/requirements.txt /project/requirements.txt

RUN apt -get update \
    && apt -get isntall -y build-essential \
    && apt -get isntall -y gettext \
    && pip install --no-cache-dir --upgrade -r /project/requirements.txt

COPY . /project

CMD ["python3", "./src/microblogging/manage.py", "runsrever"]
