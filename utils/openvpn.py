import getpass
import os
import signal
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
    p.terminate()
    # Only stdout.read actually waits until OpenVPN is finished. TODO: Check if this is POSIX-specific
    # Program stalls if server is destroyed before process is terminated.
    p.stdout.read()


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
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            wait_for_interrupt(p)
        else:
            # TODO: Find a way to retry on wrong password
            root_password = getpass.getpass(f"Root privileges required, enter password for {os.getlogin()}: ")

            # This is kinda hacky, but works since child process isn't spawned before write to stdin.
            # When debugging, the child process is spawned before and then prompts for password.
            # This seems to not be a problem IRL, but it IS a race condition that could spawn bugs in the future.
            p = subprocess.Popen(f"sudo -Sn {cmd}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            with p.stdin as pipe:
                pipe.write(root_password.encode("utf8"))
            wait_for_interrupt(p)

    else:
        print(f"Unsupported platform: {platform}")
