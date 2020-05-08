echo "Installing dockmon"

mkdir -p /opt/docker/dockmon
cd /opt/docker/dockmon

echo "- Downloading from Github"
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.yml
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/Dockerfile_dockmon
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/docker-compose.yml

echo "- Creating dockmon service"
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.service
mv /opt/docker/dockmon/dockmon.service /etc/systemd/system/dockmon.service
systemctl daemon-reload
systemctl enable node_exporter

echo "- Service created. Start by running 'service dockmon start'"