#!/usr/bin/env python3

# -*- coding: UTF-8 -*-

import pathlib
import shutil
import socket
import datetime
import json

def main():
    interfaces = []

    for _, interface_name in (socket.if_nameindex()):

        interface = {
            "name" : interface_name,
            "mac"  : None
        }

        sys_interface_dir = pathlib.Path("/sys/class/net/" + interface_name)
        sys_absolute_interface_dir = sys_interface_dir.resolve()

        if(not "pci" in str(sys_absolute_interface_dir)):
            continue

        with open(str(sys_absolute_interface_dir / "address")) as f:
            content = f.read()
            interface["mac"] = content.strip()
            interfaces.append(interface)

    interfaces = sorted(interfaces, key=lambda interface : interface["mac"])

    for index, interface in enumerate(interfaces):
        file_path = pathlib.Path("/etc/systemd/network/")
        interface["name"] = "net" + str(index)

        with open(str(file_path / ("10-" + interface["name"] + ".link")), "w") as f:
            f.write("[Match]\n")
            f.write("MACAddress=%s\n" % (interface["mac"]))
            f.write("\n")
            f.write("[Link]\n")
            f.write("Name=%s\n" % (interface["name"]))
            f.write("\n")

    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    shutil.copyfile("/etc/network/interfaces", "/etc/network/interfaces.bak__%s" % datetime_str)

    with open("/etc/network/interfaces", "w") as f:
        f.write("source /etc/network/interfaces.d/*\n")
        f.write("\n")

        f.write("auto lo\n")
        f.write("iface lo inet loopback\n")
        f.write("\n")

        for interface in interfaces:
            f.write("auto %s\n" % (interface["name"]))
            f.write("iface %s inet manual\n" % (interface["name"]))
            f.write("\n")

if(__name__ == "__main__"):
    main()
