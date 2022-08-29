import time

from fabric import Connection
from paramiko.ssh_exception import NoValidConnectionsError

from providers.base import Instance


def stabilize_connection(c):
    tries = 0
    max_tries = 10

    while tries < max_tries:
        try:
            c.run("echo Connected!")
            break
        except NoValidConnectionsError:
            print(f"Attempt failed ({tries}/{max_tries}")
            tries += 1
            time.sleep(3)
            print("Trying again...")


class Agent:
    def __init__(self):
        pass

    def install_vpn_server(self, instance: Instance, config):
        print(f"Connecting to {instance.ipv4[0]}...")
        with Connection(instance.ipv4[0], user="root", connect_kwargs={"password": instance.root_pass}) as c:
            script_url = config["agent"]["script_url"]
            stabilize_connection(c)
            c.run(f"curl {script_url} -o openvpn-install.sh")
            c.run(f"chmod +x openvpn-install.sh")
            c.run("export AUTO_INSTALL=y; ./openvpn-install.sh")
            c.run("sed -i 's/^verb [0-9]*$/verb 0/g' /etc/openvpn/server.conf")
            c.get("/root/client.ovpn")

    def vpn_connect(self):
        pass
