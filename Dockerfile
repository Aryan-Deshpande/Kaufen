FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

COPY . /app 

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "estart:app"]