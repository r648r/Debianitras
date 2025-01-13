# LACP : Debian <=> HP

## Debian 
### Setup tools

```
sudo apt update -y && apt-get install ifenslave vlan -y
echo 'bonding' > /etc/modules
modprobe bonding
echo '8021q' >> /etc/modules
modprobe 8021q
```

### Configuration file

`nano /etc/network/interfaces`

```
source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eno1
iface eno1 inet manual
	bond-master bond0

auto eno2
iface eno2 inet manual
        bond-master bond0

auto eno3
iface eno3 inet manual
        bond-master bond0

auto eno4 
iface eno4 inet manual
        bond-master bond0

auto bond0
iface bond0 inet manual
    bond-mode 4
    bond-miimon 100
    bond-slaves eno1 eno2 eno3 eno4

auto bond0.3
iface bond0.3 inet manual
    vlan-raw-device bond0
    address 10.1.1.1
    netmask 255.255.255.0
    gateway 10.1.1.254
    up ip a add 10.1.1.1/24 dev bond0.3		
    up ip r add default via 10.1.1.254 dev bond0.3
```

## HP procurve

### Command 

```
HP-2910al-48G-Switch2# conf t
HP-2910al-48G-Switch2(config)# trunk 5-8 trk2 lacp
HP-2910al-48G-Switch2(config)# int trk2
HP-2910al-48G-Switch2(eth-Trk2)# tagged vlan 3
HP-2910al-48G-Switch2(eth-Trk2)# exit
HP-2910al-48G-Switch2(config)# int 5-8
HP-2910al-48G-Switch2(eth-5-8)# enable 
HP-2910al-48G-Switch2(eth-5-8)# name "LACP to debian"
```


