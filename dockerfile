FROM python:3.7.8
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib

WORKDIR /repo/

COPY .env ./
COPY init.sh ./
COPY activate.sh ./
COPY requirements.txt ./

COPY ./src/ ./src/

RUN pip3 install -r requirements.txt

# RUN python3 ./src/db_setup/create_schemas.py

# CMD ["python3", "./src/running.py"]
RUN chmod a+x init.sh
CMD ["./init.sh"]