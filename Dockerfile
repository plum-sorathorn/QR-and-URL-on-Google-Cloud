# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Expose the port that Flask will run on
EXPOSE 8080

# Start the Flask app
CMD ["python", "app.py"]
