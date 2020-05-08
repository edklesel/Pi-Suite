# Dockmon

Dockmon is a small python script used to monitor containers using the Docker API. It multi-threads stats requests to save time, and can monitor multiple hosts specified in `dockmon.yml`.

The service uploads data to prometheus pushgateway (gateway specified in config), hopefully in future this will expand to other services such as InfluxDB.

To install, run the below command:
```bash
bash <(curl -s https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/install.sh)
```