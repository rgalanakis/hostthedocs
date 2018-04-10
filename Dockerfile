FROM python:3-alpine

ADD ./hostthedocs/ ./hostthedocs/
ADD ./.travis.yml ./.travis.yml
ADD ./MANIFEST.in ./MANIFEST.in
ADD ./conf_template.py ./conf_template.py 
ADD ./host_my_docs.py ./host_my_docs.py
ADD ./runserver.py ./runserver.py
ADD ./setup.py ./setup.py
ADD ./tox.ini ./tox.ini
ADD ./Pipfile ./Pipfile
ADD ./Pipfile.lock ./Pipfile.lock

RUN pip install pipenv
RUN pipenv install --deploy --system

ENV HTD_HOST "0.0.0.0"
ENV HTD_PORT 5000

EXPOSE 5000

CMD [ "python", "runserver.py" ]
