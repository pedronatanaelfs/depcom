FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

# Install system dependencies
RUN apt-get update && apt-get install -y python3-venv

# Create virtual environment
RUN python3 -m venv /opt/venv

# Activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Update pip and install necessary packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Register the virtual environment kernel (optional)
RUN python -m ipykernel install --user --name=venv --display-name="Python (venv)"

# Copy the rest of the application code
COPY . /app

# Startup command (adjust as needed)
CMD ["python3", "main.py"]