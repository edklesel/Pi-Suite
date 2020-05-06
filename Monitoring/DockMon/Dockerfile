FROM python:3.8

RUN pip install requests pyyaml gerequests
RUN mkdir /app
RUN cd /app
RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.py
RUN wget -q --no-check-certificate https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.yml

CMD ["python3", "dockmon.py"]