# Use lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy code
COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 80
EXPOSE 80

# Start the Flask app
CMD ["python", "app.py"]
