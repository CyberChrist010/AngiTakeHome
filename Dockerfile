FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install python3-full, and the venv module
RUN apt-get update && \
    apt-get install -y python3-full python3-venv

# Copy requirements file and the rest of your application
COPY . .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-package

# Specify the command to run on container start
CMD ["python3", "app.py"]
