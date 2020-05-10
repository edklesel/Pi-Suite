# Dockmon

Dockmon is a small python script used to monitor containers using the Docker API. It multi-threads stats requests to save time, and can monitor multiple hosts specified in `dockmon.yml`.

I created this container as the recommended application for monitoring Docker containers, cAdvisor, used up too much memory on my Raspberry Pi for not too much output, so I wrote this to fulfil my requirements.

The service uploads data to prometheus pushgateway (gateway specified in config), hopefully in future this will expand to other services such as InfluxDB.

## Install

To install, create the below files, modifying as appropriate:

### dockmon.cron

This file will control how often the job runs.

```yaml
# Run every 15 seconds
*/15 * * * * * * python3 ./dockmon.py
```

### dockmon.yml

```yaml
instance: Host                  # This is the host running dockmon
hosts:
  - name: Docker1               # Docker host 
    address: 192.168.0.1:2375   # Docker host IP address (and Docker API port)
  - name: Docker2
    address: 192.168.0.2:2375
  - name: Docker3
    address: 192.168.0.3:2375
pushgate: 192.168.0.53:9091     # Pushgate host and port
```

### docker-compose.yml

```yaml
version: '3'
services:
  dockmon: 
    image: eddi16/dockmon:latest
    container_name: dockmon
    volumes:
      - /opt/docker/dockmon/dockmon.yml:/app/dockmon.yml
      - /opt/docker/dockmon/dockmon.cron:/app/dockmon.cron
```