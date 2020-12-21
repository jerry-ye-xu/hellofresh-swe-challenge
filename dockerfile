FROM python:3.7.8
ENV PYTHONUNBUFFERED=1

WORKDIR /repo/
COPY .env ./
COPY ./src/ ./src/
COPY activate.sh ./
COPY requirements.txt ./

RUN pip3 install -r requirements.txt

# RUN python3 ./src/db_setup/create_schemas.py

# CMD ["python3", "./src/running.py"]
CMD ["python3", "./src/db_setup/create_schemas.py"]