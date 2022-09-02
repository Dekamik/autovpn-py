import getpass
import os
import subprocess
import sys


def wait_for_interrupt(p):
    pass


def connect(config, ovpn_config: str):
    platform = sys.platform
    command = config["openvpn"]["path"][platform]

    if platform.startswith("win32"):
        cmd = ["powershell", "-Command",
               f"\" Start-Process -FilePath {command} -ArgumentList --config,{ovpn_config} -Verb RunAs \""]
        with subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as p:
            print("VPN tunnel opened, press CTRL+C to exit")

            try:
                while True:
                    line = p.stdout.readline().decode("utf8")
                    err = p.stderr.readline().decode("utf8")

                    if line:
                        print(line)
                    if err:
                        print(err)
            except KeyboardInterrupt:
                pass

            print("Closing VPN tunnel...")
            p.terminate()

    elif platform.startswith("linux") or platform.startswith("darwin"):
        try:
            subprocess.run(f"{command} --config {ovpn_config}", shell=True, check=True)

        except subprocess.CalledProcessError:
            root_password = getpass.getpass(f"Root privileges required, enter password for {os.getlogin()}: ")
            subprocess.run(f"echo {root_password} | sudo -S {command} --config {ovpn_config}", stdin=subprocess.PIPE,
                           shell=True)

    else:
        print(f"Unsupported platform: {platform}")
