FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
RUN pip install --upgrade -r requirements.txt

COPY bot.py /bot.py
COPY queue_manager.py /queue_manager.py

RUN chmod 755 /bot.py
USER 1000:1000
CMD ["python", "/bot.py"]

