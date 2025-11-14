# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code
COPY server.py .

# Create a cache directory for the model (fixes permission errors)
RUN mkdir -p /app/cache
ENV HF_HOME=/app/cache
RUN chmod -R 777 /app/cache

# Expose the port Hugging Face uses
EXPOSE 7860

# Run the server
CMD ["python", "server.py"]