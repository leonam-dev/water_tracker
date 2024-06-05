FROM python:3.12-slim

WORKDIR /app

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt
RUN flask db init
RUN flask db migrate -m "initial migration"
RUN flask db upgrade

EXPOSE 5000

CMD ["python", "run.py"]