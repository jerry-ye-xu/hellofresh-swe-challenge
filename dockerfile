FROM python:3.7.8
ARG BASE_PATH=${BASEPATH}
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib

WORKDIR /repo/

COPY VERSION ./
COPY env_var ./
COPY init.sh ./
COPY activate.sh ./

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./backend_api/ ./backend_api/
RUN cd backend_api && pip3 install -e .

COPY config.py ./backend_api/instance/

# RUN python3 ./backend-api/db_setup/create_schemas.py

# CMD ["python3", "./backend-api/running.py"]
RUN chmod a+x init.sh
CMD ["./init.sh"]