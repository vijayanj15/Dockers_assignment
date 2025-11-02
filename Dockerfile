# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install Flask
RUN pip install --no-cache-dir Flask

# Make port 5000 available
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]