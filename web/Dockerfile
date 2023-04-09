FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . sentimental_analysis

CMD ["python3", "sentimental_analysis/sentiment_analysis.py"]

RUN pytest sentimental_analysis/tests/test-example.py