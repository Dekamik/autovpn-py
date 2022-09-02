import getpass
import os
import subprocess
import sys


def wait_for_interrupt(p):
    print("VPN tunnel opened, press CTRL+C to exit")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    print("Closing VPN tunnel...")
    print("This may take a couple of minutes")
    p.kill()


def connect(config, ovpn_config: str):
    platform = sys.platform
    command = config["openvpn"]["path"][platform]

    if platform.startswith("win32"):
        cmd = ["powershell", "-Command",
               f"\" Start-Process -FilePath {command} -ArgumentList --config,{ovpn_config} -Verb RunAs \""]
        p = subprocess.Popen(cmd, shell=True)
        wait_for_interrupt(p)

    elif platform.startswith("linux") or platform.startswith("darwin"):
        cmd = f"{command} --config {ovpn_config}"
        if os.geteuid() == 0:  # user is root
            p = subprocess.Popen(cmd, shell=True)
            wait_for_interrupt(p)
        else:
            root_password = getpass.getpass(f"Root privileges required, enter password for {os.getlogin()}: ")
            p = subprocess.Popen(f"sudo -S {cmd}", stdin=subprocess.PIPE, shell=True)
            with p.stdin as pipe:
                pipe.write(root_password.encode("utf8"))
            wait_for_interrupt(p)

    else:
        print(f"Unsupported platform: {platform}")
