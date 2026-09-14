FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

RUN chmod +x entrypoint.sh
RUN chown -R django:django /app

USER django