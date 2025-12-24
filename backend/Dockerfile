
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

RUN mkdir -p /app/cache
ENV HF_HOME=/app/cache
RUN chmod -R 777 /app/cache

EXPOSE 7860

CMD ["python", "server.py"]
