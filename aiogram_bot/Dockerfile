FROM python:3.10.6
ENV DATABASE_HOST=database
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
