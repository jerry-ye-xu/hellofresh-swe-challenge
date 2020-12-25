FROM python:3.7.8
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib

ARG BASE_PATH
RUN echo "BASE_PATH=${BASE_PATH}"

WORKDIR /repo/

COPY VERSION ./
COPY env_var ./
COPY init.sh ./
COPY activate.sh ./

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY "./${BASE_PATH}/" "./${BASE_PATH}/"
RUN cd $BASE_PATH && pip3 install -e .

COPY ./instance/config.py ./instance/

RUN chmod a+x init.sh
CMD ["./init.sh"]