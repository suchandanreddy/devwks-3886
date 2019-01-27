import yaml
import sys
import xmltodict
import xml.dom.minidom
from jinja2 import Template
from ncclient import manager

import logging

handler = logging.StreamHandler()
#for l in ['ncclient.transport.ssh', 'ncclient.transport.session', 'ncclient.operations.rpc']:
for l in ['ncclient.operations.rpc']:
    logger = logging.getLogger(l)
    if not logger.hasHandlers():
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)


# Load Network Configuration Details from YAML File

print("Loading Network Configuration Details from YAML File")
with open("config_details.yaml") as f:
    config = yaml.load(f.read())

# Crypto Configuration
with open("crypto_config.j2") as f:
    crypto_template = Template(f.read())


with open("interface_config.j2") as f:
    interface_template = Template(f.read())

# Create and deploy network config for all network devices

print("Processing Device Configurations")

for device in config["devices"]:
    print("Device: {}".format(device["name"]))

    # Generate Device Specific Configurations

    print("Creating Device Specific Configurations from Interface and Crypto Template")

    with open("dmvpn_spokes_config/{}_interface.cfg".format(device["name"]), "w") as f:
        interface_config = interface_template.render(interfaces=device["interfaces"])
        f.write(interface_config)

    with open("dmvpn_spokes_config/{}_dmvpn.cfg".format(device["name"]), "w") as f:
        crypto_config = crypto_template.render(VRFs=device["VRFs"],TunnelInterfaces=device["TunnelInterfaces"],ospf=device["ospf"],Profiles=device["Profiles"])
        f.write(crypto_config)



    print("Connecting to device over NETCONF")

    with manager.connect(host=device["host_ip"],
                         port=device["netconf_port"],
                         username=config["username"],
                         password=config["password"],
                         hostkey_verify=False,
                         device_params={'name': 'csr'},
                         allow_agent=False,
                         look_for_keys=False) as m:

    
        # Send NETCONF Configurations using <edit-config>
    
        print("Sending Configuration via NETCONF by using edit-config operation")
    
        interface_resp = m.edit_config(interface_config, target="running")

        crypto_resp = m.edit_config(crypto_config, target = "running")

        # Process reply XML data
    
        # print(crypto_resp)

        interface_reply = xmltodict.parse(interface_resp.xml)

        crypto_reply = xmltodict.parse(crypto_resp.xml)

        print("Interface Config: {}".format(crypto_reply["rpc-reply"]))
    
        print("DMVPN Config: {}".format(crypto_reply["rpc-reply"]))

        print("-----------------------------------------------------------------")
