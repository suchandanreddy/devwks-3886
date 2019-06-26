# DEVWKS-3886

# prerequisite

* Python 3.7+

* pip and virtualenv

* Vagrant

* VirtualBox

### Install and Setup

Clone the code to local machine.

```
git clone https://github.com/suchandanreddy/devwks-3886.git
cd devwks-3886
```

Setup Python Virtual Environment (requires Python 3.7+)

```
python3.7 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Add the vagrant box image and spin up two CSR1000v routers. ( Please note on workshop laptops we have downloaded .box already )


```
vagrant box add iosxe/16.06.04 ../serial-csr1000v-universalk9.16.06.04.box

vagrant up
```

Please configure HUB and Spoke CSR 1000v router as per below pre-config. 

HUB preconfig:

```
vagrant ssh iosxe1

conf t

hostname HUB

vrf definition RED
 !
 address-family ipv4
 exit-address-family
 !

crypto isakmp policy 1
 authentication pre-share
crypto isakmp key cisco47 address 0.0.0.0
crypto ipsec transform-set trans2 esp-des esp-md5-hmac
 mode transport
crypto ipsec profile vpnprof
 set transform-set trans2

interface Tunnel0
 bandwidth 1000
 vrf forwarding RED
 ip address 10.0.0.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication test
 ip nhrp network-id 100000
 ip ospf network broadcast
 ip ospf priority 2
 delay 1000
 tunnel source GigabitEthernet2
 tunnel mode gre multipoint
 tunnel key 100000
 tunnel protection ipsec profile vpnprof

interface GigabitEthernet2
 ip address 10.10.10.1 255.255.255.0
 negotiation auto

do wr mem
```

Spoke Preconfig:

```
vagrant ssh iosxe2

conf t

hostname spoke

ip access-list extended 104
permit ip host 1.1.1.1 any

do wr mem
```

Start the jupyter notebook and open localhost:8888 in browser to access netconf.ipynb and restconf.ipynb

```
jupyter notebook
```
