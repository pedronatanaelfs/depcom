FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git vim build-essential

# Copy requirements.txt
COPY requirements.txt ./

# Upgrade pip and install packages
RUN python3 -m pip install --upgrade pip  && python3 -m pip install -r requirements.txt
