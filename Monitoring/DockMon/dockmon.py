import requests
import yaml
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

with open('dockmon.yml','r') as conf:
        config = yaml.load(conf,Loader=yaml.FullLoader)

hosts = config['hosts']
interval = config['interval']

types = {
    'container_mem_usage': '# TYPE container_mem_usage gauge',
    'container_mem_lim': '# TYPE container_mem_lim gauge',
    'container_mem_max': '# TYPE container_mem_max gauge',
    'container_mem_usage_pc': '# TYPE container_mem_usage_pc gauge',
    'container_mem_max_pc': '# TYPE container_mem_max_pc gauge',
    'container_cpu_usage': '# TYPE container_cpu_usage gauge',
    'container_cpu_usage_pre': '# TYPE container_cpu_usage_pre gauge',
    'container_cpu_usage_sys': '# TYPE container_cpu_usage_sys gauge',
    'container_cpu_usage_pre_sys': '# TYPE container_cpu_usage_pre_sys gauge',
    'container_cpu_usage_perc': '# TYPE container_cpu_usage_perc gauge',
    'container_bytes_i': '# TYPE container_bytes_i gauge',
    'container_bytes_o': '# TYPE container_bytes_o gauge',
    'container_packets_i': '# TYPE container_packets_i gauge',
    'container_packets_o': '# TYPE container_packets_o gauge'
}

data = {
    'container_mem_usage': [],
    'container_mem_lim': [],
    'container_mem_max': [],
    'container_mem_usage_pc': [],
    'container_mem_max_pc': [],
    'container_cpu_usage': [],
    'container_cpu_usage_pre': [],
    'container_cpu_usage_sys': [],
    'container_cpu_usage_pre_sys': [],
    'container_cpu_usage_perc': [],
    'container_bytes_i': [],
    'container_bytes_o': [],
    'container_packets_i': [],
    'container_packets_o': []
}

def get_stats(host):

    # Get list of containers running on host
    containers = requests.get((f'http://{host}/containers/json')).json()

    # Function to get the stats for a given container
    def get_container_stats(host, container):
        return requests.get(f"http://{host}/containers/{container['Names'][0][1:]}/stats?stream=False")

    # Multi-thread the requests to the host to get the tats
    with ThreadPoolExecutor(max_workers=20) as executor:
        processes = [executor.submit(get_container_stats,host,container) for container in containers]

    # Return the json data from the request
    return [task.result().json() for task in as_completed(processes)]

    #return [response.json() for response in responses]


while True:

    # Cycle through each host in the config
    for host in hosts:
        
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

            data['container_mem_usage'].append(f'container_mem_usage{{container="{container_name}"}} {mem_usage}')
            data['container_mem_lim'].append(f'container_mem_lim{{container="{container_name}"}} {mem_lim}')
            data['container_mem_max'].append(f'container_mem_max{{container="{container_name}"}} {mem_max}')
            data['container_mem_usage_pc'].append(f'container_mem_usage_pc{{container="{container_name}"}} {mem_usage_pc}')
            data['container_mem_max_pc'].append(f'container_mem_max_pc{{container="{container_name}"}} {mem_max_pc}')


            # Container CPU stats
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            cpu_usage_pre = stats['precpu_stats']['cpu_usage']['total_usage']
            cpu_usage_sys = stats['cpu_stats']['system_cpu_usage']
            cpu_usage_pre_sys = stats['precpu_stats']['system_cpu_usage']
            cpu_usage_perc = 100 * (cpu_usage - cpu_usage_pre) / (cpu_usage_sys - cpu_usage_pre_sys)

            data['container_cpu_usage'].append(f'container_cpu_usage{{container="{container_name}"}} {cpu_usage}')
            data['container_cpu_usage_pre'].append(f'container_cpu_usage_pre{{container="{container_name}"}} {cpu_usage_pre}')
            data['container_cpu_usage_sys'].append(f'container_cpu_usage_sys{{container="{container_name}"}} {cpu_usage_sys}')
            data['container_cpu_usage_pre_sys'].append(f'container_cpu_usage_pre_sys{{container="{container_name}"}} {cpu_usage_pre_sys}')
            data['container_cpu_usage_perc'].append(f'container_cpu_usage_perc{{container="{container_name}"}} {cpu_usage_perc}')


            # Container network stats
            for interface in stats['networks']:

                bytes_i = stats['networks'][interface]['rx_bytes']
                bytes_o = stats['networks'][interface]['tx_bytes']
                packets_i = stats['networks'][interface]['rx_packets']
                packets_o = stats['networks'][interface]['tx_packets']
                
                data['container_bytes_i'].append(f'container_bytes_i{{container="{container_name}",interface="{interface}"}} {bytes_i}')
                data['container_bytes_o'].append(f'container_bytes_o{{container="{container_name}",interface="{interface}"}} {bytes_o}')
                data['container_packets_i'].append(f'container_packets_i{{container="{container_name}",interface="{interface}"}} {packets_i}')
                data['container_packets_o'].append(f'container_packets_o{{container="{container_name}",interface="{interface}"}} {packets_o}')

        # Collate data into a request body
        prom_body = ''
        for metric in data:
            prom_body += f"{types[metric]}" + '\n' + '\n'.join(data[metric]) + '\n\n'

        # Post results to Pushgateway
        r = requests.post(
            url=f"http://{config['pushgate']}/metrics/job/dockmon/instance/{host_name}",
            headers={"Content-Type": "text/plain"},
            data=prom_body
        )
        
    sleep(config['interval'])