import subprocess
import sys
import time

from fabric import Connection
from paramiko.ssh_exception import NoValidConnectionsError

from providers.base import Instance


def stabilize_connection(c: Connection, max_retries: int, sleep_seconds: int):
    attempt = 0
    while attempt < max_retries:
        try:
            c.run("echo Connected!")
            break
        except (NoValidConnectionsError, TimeoutError):
            attempt += 1
            print(f"Attempt {attempt}/{max_retries} failed")
            time.sleep(sleep_seconds)
            print("Retrying...")


def install_vpn_server(instance: Instance, config):
    print(f"Connecting to {instance.ipv4[0]}...")

    with Connection(instance.ipv4[0], user="root", connect_kwargs={"password": instance.root_pass}) as c:
        script_url = config["agent"]["script_url"]
        max_retries = config["agent"]["max_retries"]
        sleep_seconds = config["agent"]["sleep_seconds"]

        stabilize_connection(c, max_retries, sleep_seconds)

        c.run(f"curl {script_url} -o openvpn-install.sh")
        c.run("chmod +x openvpn-install.sh")
        c.run("export AUTO_INSTALL=y; ./openvpn-install.sh")
        c.run("sed -i 's/^verb [0-9]*$/verb 0/g' /etc/openvpn/server.conf")
        c.get("/root/client.ovpn")


def vpn_connect(config, ovpn_config: str):

    if sys.platform.startswith("win32"):
        pass
    else:
        with subprocess.Popen(["openvpn", "-c", ovpn_config]) as p:
            pass
