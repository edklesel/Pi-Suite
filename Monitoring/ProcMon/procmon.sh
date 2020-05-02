#!/bin/bash
while sleep 1; do
url="http://localhost:9091/metrics/job/top/instance/$(hostname)"
cpuvar="# TYPE proc_cpu gauge
"
memvar="# TYPE proc_mem gauge
"
cpuvar=$cpuvar$(ps --no-headers -e -o comm,pid,%cpu --sort=-%cpu | head -n 10 | awk '{print "proc_cpu{process=\""$1"\", pid=\""$2"\"}", $3}')
memvar=$memvar$(ps --no-headers -e -o comm,pid,%mem --sort=-%mem | head -n 10 | awk '{print "proc_mem{process=\""$1"\", pid=\""$2"\"}", $3}')
curl -X POST -H  "Content-Type: text/plain" --data "$cpuvar
" $url
curl -X POST -H  "Content-Type: text/plain" --data "$memvar
" $url
done;
