from requests import get, post
from yaml import load, FullLoader
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed


with open('dockmon.yml','r') as conf:
    config = load(conf,Loader=FullLoader)

hosts = config['hosts']

with open('metrics.yml', 'r') as f:
    metrics = load(f,Loader=FullLoader)

data = {f"{metric}": [] for metric in metrics}

def format_stat(host, container, metric, statval, **kwargs):

    data = f'{metric}{{host="{host}",container="{container}"'

    for key, value in kwargs.items():
        data += f',{key}="{value}"'

    data += f'}} {statval}'

    return data

def get_stats(host):

    # Get list of containers running on host
    containers = get((f'http://{host}/containers/json')).json()

    # If there are no containers, just return an empty array
    if containers == []:
        return []
        
    # Function to get the stats for a given container
    def get_container_stats(host, container):
        return get(f"http://{host}/containers/{container['Names'][0][1:]}/stats?stream=False")

    # Multi-thread the requests to the host to get the tats
    with ThreadPoolExecutor(max_workers=20) as executor:
        processes = [executor.submit(get_container_stats,host,container) for container in containers]

    # Return the json data from the request
    return [task.result().json() for task in as_completed(processes)]


# Cycle through each host in the config
for host in hosts:
    
    # Host name of the host
    host_name = host['name']

    # Get an array of stats for all the containers
    container_stats = get_stats(host=host['address'])
    # Loop through the stats for each container
    for stats in container_stats:
        container_name = stats['name'][1:]
        # Container memory stats
        mem_usage = stats['memory_stats']['usage']
        mem_lim = stats['memory_stats']['limit']
        mem_max = stats['memory_stats']['max_usage']
        mem_usage_pc = mem_usage / mem_lim
        mem_max_pc = mem_max / mem_lim
        data['container_mem_usage'].append(format_stat(host=host_name,container=container_name,metric='container_mem_usage',statval=mem_usage))
        data['container_mem_lim'].append(format_stat(host=host_name,container=container_name,metric='container_mem_lim',statval=mem_lim))
        data['container_mem_max'].append(format_stat(host=host_name,container=container_name,metric='container_mem_max',statval=mem_max))
        data['container_mem_usage_pc'].append(format_stat(host=host_name,container=container_name,metric='container_mem_usage_pc',statval=mem_usage_pc))
        data['container_mem_max_pc'].append(format_stat(host=host_name, container=container_name, metric='container_mem_max_pc', statval=mem_max_pc))
        
        # Container CPU stats
        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        cpu_usage_pre = stats['precpu_stats']['cpu_usage']['total_usage']
        cpu_usage_sys = stats['cpu_stats']['system_cpu_usage']
        cpu_usage_pre_sys = stats['precpu_stats']['system_cpu_usage']
        cpu_usage_perc = 100 * (cpu_usage - cpu_usage_pre) / (cpu_usage_sys - cpu_usage_pre_sys)
        data['container_cpu_usage'].append(format_stat(host=host_name, container=container_name, metric='container_cpu_usage', statval=cpu_usage))
        data['container_cpu_usage_pre'].append(format_stat(host=host_name, container=container_name, metric='container_cpu_usage_pre', statval=cpu_usage_pre))
        data['container_cpu_usage_sys'].append(format_stat(host=host_name, container=container_name, metric='container_cpu_usage_sys', statval=cpu_usage_sys))
        data['container_cpu_usage_pre_sys'].append(format_stat(host=host_name, container=container_name, metric='container_cpu_usage_pre_sys', statval=cpu_usage_pre_sys))
        data['container_cpu_usage_perc'].append(format_stat(host=host_name, container=container_name, metric='container_cpu_usage_perc', statval=cpu_usage_perc))
        
        # Container network stats
        for interface in stats['networks']:
            bytes_i = stats['networks'][interface]['rx_bytes']
            bytes_o = stats['networks'][interface]['tx_bytes']
            packets_i = stats['networks'][interface]['rx_packets']
            packets_o = stats['networks'][interface]['tx_packets']
            
            data['container_bytes_i'].append(format_stat(host=host_name, container=container_name, metric='container_bytes_i', statval=bytes_i,interface=interface))
            data['container_bytes_o'].append(format_stat(host=host_name, container=container_name, metric='container_bytes_o', statval=bytes_o,interface=interface))
            data['container_packets_i'].append(format_stat(host=host_name, container=container_name, metric='container_packets_i', statval=packets_i,interface=interface))
            data['container_packets_o'].append(format_stat(host=host_name, container=container_name, metric='container_packets_o', statval=packets_o,interface=interface))

# Collate data into a request body
prom_body = ''
for metric in metrics:
    prom_body += f"# HELP {metric} {metrics[metric]['help']}" + '\n' + f"# TYPE {metric} {metrics[metric]['type']}" + '\n' + '\n'.join(data[metric]) + '\n\n'
# Post results to Pushgateway
r = post(
    url=f"http://{config['pushgate']}/metrics/job/dockmon/instance/{config['instance']}",
    headers={"Content-Type": "text/plain"},
    data=prom_body
)