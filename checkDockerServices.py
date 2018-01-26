import consul
import docker
import os
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

############################
## Set up logging mechanism
#############################
logging.basicConfig()
alfred = logging.getLogger("Key/Value to Consul Script")

###################################
## Check for environment variables
## Exit(1) and log error if vars 
## do not exist
##################################
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

##################################
## Connect to local docker daemon
##################################
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

##################################
## Get list of services in swarm
##################################
services = client.services.list()

##################################
## Loop through each service and
## check label inventory
## If cron : true, then grab....
## Write the collecte key/value
## pair to Consul and log success
##################################
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

