FROM nginx:1.25.3
#MAINTAINER Jonathan Arrance <jonathan@thesingleboard.io>

ENV INSTALL_PATH /opt/homebot

RUN apt-get update -y;apt-get install -y curl;apt-get install -y python;apt install -y sqlite3;apt-get install -y python3-pip;apt install -y python3-dev;apt install -y vim;apt install -y htop

WORKDIR $INSTALL_PATH

RUN mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

COPY ./nginx-default.conf /nginx-default.conf

ADD coinbase.py $INSTALL_PATH
ADD crypto_lib.py $INSTALL_PATH
ADD run_app.py $INSTALL_PATH
ADD entrypoint.sh $INSTALL_PATH
ADD settings.py $INSTALL_PATH
ADD database.py $INSTALL_PATH
ADD api.py $INSTALL_PATH
ADD prom_lib.py $INSTALL_PATH

ENTRYPOINT ["python3","run_app.py"]
