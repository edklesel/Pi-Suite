FROM alpine:latest

RUN apk add --update-cache python3

RUN mkdir /app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install pyyaml

RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.py
RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.yml

CMD ["python3", "dockmon.py"]