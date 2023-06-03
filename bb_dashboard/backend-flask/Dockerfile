FROM python:3.8.1-slim-buster

RUN pip3 install --upgrade pip

# COPY main.py requirements.txt config.py .env ./
WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

# ENTRYPOINT ["python3"]
# CMD ["app.py"]
