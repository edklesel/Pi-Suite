#!/bin/bash
cd /tmp
read -p "Pushgate Host IP Address: " pushgatehost
echo ""
echo "Installing ProcMon..."
echo "- Downloading procmon from GitHub."
wget -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/ProcMon/procmon.sh
echo "- Moving procmon to /opt/monitoring/procmon"
chmod u+x procmon
mkdir -p /opt/monitoring/procmon
mv procmon.sh /opt/monitoring/procmon
sed -i "s/<procmonhost>/$pushgatehost/g" /opt/monitoring/procmon/procmon

echo "- Downloading procmon service file"
wget -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/ProcMon/procmon.service
echo "- Moving service file to systemd"
mv procmon.service /etc/systemd/system/procmon.service
echo "- Reloading systemctl daemon"
systemctl daemon-reload
echo "Fin"