FROM python:3.8-slim

RUN mkdir /app
RUN cd /app
RUN pip install requests pyyaml

RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.py
RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.yml

CMD ["python3", "dockmon.py"]