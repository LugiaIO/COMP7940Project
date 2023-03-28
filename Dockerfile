FROM python:3.8-slim
ARG ACCESS_TOKEN
ENV TOKEN=$ACCESS_TOKEN
RUN echo "The ENV variable value is $TOKEN"
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./
RUN   echo "Some line to add to a file" >> ./config.ini
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 bot:app