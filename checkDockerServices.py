import consul
import docker
import os
import logging

logging.basicConfig()
alfred = logging.getLogger("Key/Value to Consul Script")

from requests.packages.urllib3.exceptions import InsecureRequestWarning

if "CONSULIP" in os.environ:
    consulIP = os.getenv("CONSULIP")
else:
    alfred.error("Please set Environment Variable: CONSULIP: <consul IP address>")
    exit(1)
    
if "CONSULPORT" in os.environ:
    consulPort = os.getenv("CONSULPORT")
else:
    alfred.error("Please set Environment Variable: CONSULPORT: <consul Port>")
    exit(1)

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
services = client.services.list()

for service in services:
    serviceObject = service.attrs
    # get label
    labels = serviceObject["Spec"]["Labels"]
    print(labels)
    try:
        if labels["cron"] == True:
            labelKey = "CronSchedule"
            labelValue = labels["CronSchedule"]

    except:
            continue

    c = consul.Consul(host=consuIP, port=consulPort, scheme='https',verify=False)
    c.kv.put(labelKey, labelValue)
    alfred.info("Added {0}:{1} key-value pair to Consul".format(labelKey, labelValue))

