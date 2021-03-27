#!/usr/bin/env python3

import pathlib
import os
import shutil

def main():
    modules_dir = pathlib.Path(__file__).parent.absolute() / "modules"

    lib_modules_dir = pathlib.Path("/lib/modules/")
    for dir in lib_modules_dir.glob("*/"):
        if(not dir.is_dir()):
            continue

        realtek_dir = dir / "kernel" / "drivers" / "net" / "phy"
        if(realtek_dir.exists()):
            shutil.copy(
                str(modules_dir / "realtek.ko"),
                str(realtek_dir / "realtek.ko")
            )
        
        r8169_dir = dir / "kernel" / "drivers" / "net" / "ethernet" / "realtek"
        if(r8169_dir.exists()):
            shutil.copy(
                str(modules_dir / "r8169.ko"),
                str(r8169_dir   / "r8169.ko")
            )
            
    lib_rtl_nic_dir = pathlib.Path("/lib/firmware/rtl_nic/")
    shutil.copy(
        str(modules_dir     / "rtl8125b-2.fw"),
        str(lib_rtl_nic_dir / "rtl8125b-2.fw")
    )


    os.system("rmmod r8169")
    os.system("rmmod r8125")
    os.system("rmmod realtek")

    os.system("modprobe realtek")
    os.system("modprobe r8169")

    os.system("update-initramfs -u")

    
if(__name__ == "__main__"):
    main()
    
