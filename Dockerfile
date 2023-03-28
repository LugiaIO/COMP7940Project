FROM python:3.8-slim
ARG TEST1
ENV TEST2=$TEST1
RUN echo "The ENV variable value is $TEST2"
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 bot:app