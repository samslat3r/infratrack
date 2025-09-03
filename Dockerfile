# App image: Flask served by Gunicorn
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt && pip cache purge

COPY . /app

# Defaults overridden by .env
ENV FLASK_APP=run.py \
    HOST=0.0.0.0 \
    PORT=5000

EXPOSE 5000

# Gunicorn (development) (reload will pick up code changes)
CMD ["gunicorn", "--reload", "-w", "2", "-k", "gthread", "-b", "0.0.0.0:5000", "run:app"]