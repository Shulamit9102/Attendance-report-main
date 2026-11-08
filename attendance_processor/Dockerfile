FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . .

# Set PYTHONPATH environment variable
ENV PYTHONPATH=.

# Default command to run the application
CMD ["python", "main.py"]