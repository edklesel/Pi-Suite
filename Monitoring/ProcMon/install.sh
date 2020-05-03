echo "Installing ProcMon..."
cd /tmp
read -p "Pushgate Host IP Address: " pushgatehost
wget https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/ProcMon/procmon.sh
mv procmon.sh procmon
chmod u+x procmon
mkdir/opt/monitoring
mkdir /opt/monitoring/procmon
mv procmon /opt/monitoring/procmon
sed -i "s/<procmonhost>/$pushgatehost/g" /opt/monitoring/procmon/procmon

wget https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/ProcMon/procmon.service
mv procmon.service /etc/systemd/system/procmon.service
systemctl daemon-reload
