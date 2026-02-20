FROM python:3.11.4-slim-bullseye

WORKDIR /app
COPY . /app

ENV PLAYWRIGHT_BROWSERS_PATH=/playwright-browsers

RUN apt-get update -y || (sleep 5 && apt-get update -y) \
    && pip install --upgrade pip --default-timeout=100 \
    && pip install -r requirements.txt --default-timeout=100 \
    && playwright install --with-deps chromium \
    && chmod -Rf 777 $PLAYWRIGHT_BROWSERS_PATH

ENV SCRAPY_SETTINGS_MODULE scrapy_playwright_ato.settings
RUN python setup.py install
