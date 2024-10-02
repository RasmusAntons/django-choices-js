FROM python:3.12-slim

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install uvicorn
COPY . /app
RUN pip install /app
WORKDIR /app/example
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000/tcp
ENTRYPOINT ["uvicorn", "example.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
