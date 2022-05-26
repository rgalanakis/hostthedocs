FROM python:3.6-alpine
RUN pip install pipenv

ADD ./Pipfile ./Pipfile
ADD ./Pipfile.lock ./Pipfile.lock

RUN pipenv install --deploy --system

ADD ./hostthedocs/ ./hostthedocs/
ADD ./runserver.py ./runserver.py

ENV HTD_HOST "0.0.0.0"
ENV HTD_PORT 5000

EXPOSE 5000

CMD [ "python", "runserver.py" ]
