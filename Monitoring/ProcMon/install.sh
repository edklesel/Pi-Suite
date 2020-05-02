echo "Installing ProcMon..."
cd /tmp
wget https://github.com/edklesel/Pi-Suite/Monitoring/ProcMon/procmon.sh
mv procmon.sh procmon
chmod u+x procmon
mkdir/opt/monitoring
mkdir /opt/monitoring/procmon
mv procmon /opt/monitoring/procmon

wget https://github.com/edklesel/Pi-Suite/Monitoring/ProcMon/procmon.service
mv procmon.service /etc/systemd/system/procmon.service
systemctl daemon-reload
