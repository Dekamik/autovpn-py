import getpass
import os
import subprocess
import sys


def connect(config, ovpn_config: str):
    platform = sys.platform
    command = config["openvpn"]["path"][platform]

    if platform.startswith("win32"):
        ps_command = r"Powershell -Command \"& { Start-Process -FilePath \"" + command + \
                     r"\" -ArgumentList \"--config\",\"" + ovpn_config + r"\" -Verb RunAs }\""
        subprocess.run(ps_command, shell=True, check=True)

    elif platform.startswith("linux") \
            or platform.startswith("darwin"):
        try:
            subprocess.run(f"{command} --config {ovpn_config}", stdin=subprocess.PIPE, shell=True, check=True)

        except subprocess.CalledProcessError:
            root_password = getpass.getpass(f"Root privileges required, enter password for {os.getlogin()}:")
            subprocess.run(f"echo {root_password} | sudo -S {command} --config {ovpn_config}", shell=True, check=True)

    else:
        print(f"Unsupported platform: {platform}")
