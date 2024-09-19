FROM python:3.9

WORKDIR /app

RUN apt update && apt install -y git vim

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

COPY . /app

CMD ["python3", "main.py"]
