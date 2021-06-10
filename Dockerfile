FROM python:3.8-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir \
    && rm requirements.txt
CMD python app.py