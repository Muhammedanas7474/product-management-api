# --------- BUILDER STAGE ---------
FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# --------- FINAL STAGE ---------
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    netcat-openbsd \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 8000
EXPOSE 5555

CMD ["sh", "/app/entrypoint.sh"]
