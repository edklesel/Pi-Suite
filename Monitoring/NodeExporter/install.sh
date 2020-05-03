#!/bin/bash
echo ""
echo "Installing node_exporter"
version="node_exporter-0.18.1.linux-armv7"

echo "- Downloading from github"
wget --no-check-certificate -q "https://github.com/prometheus/node_exporter/releases/download/v0.18.1/${version}.tar.gz"

echo "- Extracting tarball"
mkdir -p /opt/monitoring
tar -xzf "${version}.tar.gz" -C /opt/monitoring
mv "/opt/monitoring/$version" /opt/monitoring/node_exporter
rm "${version}.tar.gz" -rf

echo "- Creating node_exporter service"
wget --no-check-certificate -q https://raw.githubusercontent.com/edklesel/Pi-Suite/master/Monitoring/NodeExporter/node_exporter.service
mv node_exporter.service /etc/systemd/system
systemctl daemon-reload
systemctl enable node_exporter

echo "- Service created. Start by running 'service node_exporter start'"