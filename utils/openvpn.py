import getpass
import os
import subprocess
import sys


def connect(config, ovpn_config: str):
    platform = sys.platform
    command = config["openvpn"]["path"][platform]

    try:
        subprocess.run(f"sudo {command} --config {ovpn_config}", stdin=subprocess.PIPE, shell=True, check=True)
    except subprocess.CalledProcessError:
        root_password = getpass.getpass(f"Higher privileges required, enter password for {os.getlogin()}:")
        subprocess.run(f"echo {root_password} | sudo -S {command} --config {ovpn_config}", stdin=subprocess.PIPE,
                       shell=True, check=True)
