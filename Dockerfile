FROM python:3.12

RUN pip install --no-cache-dir --upgrade pip setuptools

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt

COPY . .