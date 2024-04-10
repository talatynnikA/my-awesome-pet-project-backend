FROM python:3.9-slim

WORKDIR /app
RUN python -m venv venv
# RUN source venv/bin/activate
COPY requirements.txt .
RUN venv/bin/pip install -r requirements.txt

#RUN pip install -r requirements.txt

ENV DB_USERNAME $postgres_user
ENV DB_PASSWORD $postgres_pass
ENV DB_URI $database_name

RUN venv/bin/flask db upgrade

#RUN flask run
COPY . .
EXPOSE 5000
CMD ["venv/bin/flask", "run", "--host=0.0.0.0"]
