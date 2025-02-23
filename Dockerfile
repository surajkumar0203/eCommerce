FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONBUFFERED=1

WORKDIR /Ecommerce

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 8000