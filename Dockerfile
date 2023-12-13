FROM python:3.8.10

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

COPY . .
