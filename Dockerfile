FROM python:3.9-alpine

RUN apk update

RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock bootstrap.sh request_json_validation.py request_logic.py requests.py ./

RUN pipenv install

EXPOSE 5000:5000

ENTRYPOINT ["/usr/src/app/bootstrap.sh"]