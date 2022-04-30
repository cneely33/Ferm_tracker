# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080

EXPOSE 8080 80 $PORT

#CMD ["python3", "./index.py"]
#CMD [ "gunicorn", "--workers=3", "--threads=1", "-b 0.0.0.0:8080", "index:server"]
#CMD [ "gunicorn", "--workers=3", "--threads=1", "-b 0.0.0.0:$PORT", "index:server"]
CMD gunicorn --workers=3 --threads=1 -b 0.0.0.0:$PORT index:server
