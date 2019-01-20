import yaml
import sys
import xmltodict
import xml.dom.minidom
from jinja2 import Template
from ncclient import manager

import logging

handler = logging.StreamHandler()
for l in ['ncclient.transport.ssh', 'ncclient.transport.session', 'ncclient.operations.rpc']:
    logger = logging.getLogger(l)
    if not logger.hasHandlers():
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

delete_interface_template = '''
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
            <name>Tunnel0</name>
        </interface>
    </interfaces>
</config>'''

for device in config["devices"]:

    print("Device: {}".format(device["name"]))

    print("Deleting Tunnel interface Configurations using Templates")

    with manager.connect(host=device["host_ip"],
                         port=device["netconf_port"],
                         username=config["username"],
                         password=config["password"],
                         hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False,
                         look_for_keys=False) as m:

        netconf_reply = m.edit_config(delete_interface_template,target='running')

        print(netconf_reply)
        print("-----------------------------------------------------------------")

delete_crypto_template = '''<config>    
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <crypto>
        <ipsec xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-crypto">
            <profile operation="delete">
                <name>vpnprof</name>
            </profile>
            </ipsec>
    </crypto>
    </native>
    </config>'''

for device in config["devices"]:

    print("Device: {}".format(device["name"]))

    print("Deleting Crypto ipsec profile Configurations using Templates")
    
    with manager.connect(host=device["host_ip"],
                         port=device["netconf_port"],
                         username=config["username"],
                         password=config["password"],
                         hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False,
                         look_for_keys=False) as m:
        
        netconf_reply = m.edit_config(delete_crypto_template,target='running')
        print(netconf_reply)
        print("-----------------------------------------------------------------")

           
delete_transformset_template = '''<config>    
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <crypto>
            <ipsec xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-crypto">
            <transform-set operation="delete">
                    <tag>trans2</tag>
                    <esp>esp-des</esp>
                    <esp-hmac>esp-md5-hmac</esp-hmac>
                    <mode>
                        <transport/>
                    </mode>
                </transform-set>
            </ipsec>
            <isakmp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-crypto">
                <key operation="delete">
                    <key-address>
                        <key>cisco47</key>
                        <addr4-container>
                            <address>0.0.0.0</address>
                        </addr4-container>
                    </key-address>
                </key>
                <policy operation="delete">
                    <number>1</number>
                    <authentication>pre-share</authentication>
                </policy>
            </isakmp>
    </crypto>
    </native>
    </config>'''

for device in config["devices"]:

    print("Device: {}".format(device["name"]))

    print("Deleting Crypto transform Set Configurations using Templates")

    with manager.connect(host=device["host_ip"],
                         port=device["netconf_port"],
                         username=config["username"],
                         password=config["password"],
                         hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False,
                         look_for_keys=False) as m:
      
        netconf_reply = m.edit_config(delete_transformset_template,target='running')
        print(netconf_reply)
        print("-----------------------------------------------------------------")    
