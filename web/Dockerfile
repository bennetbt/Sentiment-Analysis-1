FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . web/
#COPY -r ../sentimental_analysis webs/


CMD ["python3", "web/frontend.py"]

#RUN pytest web/tests/test-frontend.py