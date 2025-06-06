FROM python:3.11.7-bookworm
RUN apt-get update && apt-get install python3-tk tk-dev -y
COPY pyproject.toml /usr/local/src/myscripts/pyproject.toml
COPY poetry.lock /usr/local/src/myscripts/poetry.lock
WORKDIR /usr/local/src/myscripts/
RUN pip install --upgrade pip && pip install poetry && poetry self add poetry-plugin-export && poetry export -o requirements.txt && pip install -r requirements.txt
COPY ./code/backend /usr/local/src/myscripts/
# https://github.com/docker/buildx/issues/2751
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/src/myscripts/"
EXPOSE 80
CMD ["streamlit", "run", "Admin.py", "--server.port", "80", "--server.enableXsrfProtection", "false"]
