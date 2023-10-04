FROM python:3.10-slim

WORKDIR /app

COPY ../../app.requirements.txt .
RUN pip install --no-cache-dir -r app.requirements.txt

COPY . .

CMD ["python", "app.py"]

