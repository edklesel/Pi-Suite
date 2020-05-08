# Dockmon

Dockmon is a small python script used to monitor containers using the Docker API. It multi-threads stats requests to save time, and can monitor multiple hosts specified in `dockmon.yml`.

I created this container as the recommended application for monitoring Docker containers, cAdvisor, used up too much memory on my Raspberry Pi for not too much output, so I wrote this to fulfil my requirements.

The service uploads data to prometheus pushgateway (gateway specified in config), hopefully in future this will expand to other services such as InfluxDB.

To install, run the below command:
```bash
bash <(curl -s https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/install.sh)
```