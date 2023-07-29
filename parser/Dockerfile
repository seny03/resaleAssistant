FROM python:3.10-bullseye

ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
