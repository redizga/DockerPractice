FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY sensor.py main.py ./
CMD ["python", "main.py"]
