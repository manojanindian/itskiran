# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /itskiran

# Copy dependencies
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app .

# Run app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
