#!/bin/bash

sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

CODENAME=`cat /etc/os-release |grep CODENAME |cut -f 2 -d "="`
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve $CODENAME pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list

cp /usr/share/perl5/PVE/APLInfo.pm /usr/share/perl5/PVE/APLInfo.pm_back
sed -i 's|http://download.proxmox.com|https://mirrors.ustc.edu.cn/proxmox|g' /usr/share/perl5/PVE/APLInfo.pm

sed -i 's/^/#/g' /etc/apt/sources.list.d/pve-enterprise.list

apt update -y
apt upgrade -y

apt install \
    git \
    zsh \
    emacs \
    isc-dhcp-server \
    tmux \
    -y

cat << EOF > /etc/dhcp/dhcpd.conf
option domain-name-servers 223.5.5.5, 223.6.6.6;
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
subnet 10.0.0.0 netmask 255.255.255.0 {
  range 10.0.0.10 10.0.0.254;
  option routers 10.0.0.1;
  option broadcast-address 10.0.0.255;
}
EOF

sed -i 's/INTERFACESv4=""/INTERFACESv4="net1"/g' /etc/default/isc-dhcp-server

cat << EOF >> /etc/network/interfaces
    #post-up   iptables -t nat -A POSTROUTING -o net1 -j MASQUERADE
    #post-down iptables -t nat -D POSTROUTING -o net1 -j MASQUERADE
EOF

crontab -l | { cat; echo "* * * * *  echo \`date\` '|'  \`uptime -s\` >> /var/log/uptime.log"; } | crontab -

