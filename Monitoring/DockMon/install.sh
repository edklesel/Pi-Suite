echo "Installing dockmon"

mkdir -p /opt/docker/dockmon
cd /opt/docker/dockmon

echo "- Downloading from Github"
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.yml
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/dockmon.cron
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/DockMon/docker-compose.yml
