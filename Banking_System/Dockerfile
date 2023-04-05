FROM python:3.9.6-slim-buster

WORKDIR /bank_app

COPY . ./

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r /bank_app/requirements.txt  --no-cache-dir
RUN python manage.py makemigrations
RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "Banking_System.wsgi:application", "--bind", "0.0.0.0:8000"]

