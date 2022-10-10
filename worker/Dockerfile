FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
RUN pip install --upgrade -r requirements.txt

COPY worker.py /worker.py
USER 1000:1000
CMD ["python", "/worker.py"]