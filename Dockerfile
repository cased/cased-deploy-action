FROM python:3.12-slim

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY index.py /action/index.py
ENTRYPOINT ["python3", "/action/index.py"]