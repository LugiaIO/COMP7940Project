FROM python:3.8-slim
ARG ACCESS_TOKEN
ENV TOKEN=$ACCESS_TOKEN
RUN echo "The ENV variable value is $TOKEN"
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./
CMD ["gunicorn", "bot:app", "--config=config.py", "--worker-class=gevent", "--timeout=5"]