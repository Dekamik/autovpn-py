import getpass
import os
import subprocess
import sys


def wait_for_interrupt(p, platform):
    if platform.startswith("win32"):
        print("VPN tunnel opened. To exit: close external window, then press CTRL+C in this window")
    else:
        print("VPN tunnel opened, press CTRL+C to exit")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    if not platform.startswith("win32"):
        print("Closing VPN tunnel...")
        p.terminate()
        # Only stdout.read actually waits until OpenVPN is finished.
        # WARNING: Program stalls if server is destroyed before process is terminated.
        p.stdout.read()


def connect_win(command, ovpn_config):
    cmd = ["Powershell", "Start", f"\"{command}\"", "-ArgumentList", f"--config,{ovpn_config}", "-Verb", "RunAs"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    wait_for_interrupt(p, "win32")


def connect_posix(command, ovpn_config, platform):
    cmd = f"{command} --config {ovpn_config}"

    if os.geteuid() == 0:  # user is root
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    else:
        # TODO: Find a way to test and retry passwords
        root_password = getpass.getpass(f"Root privileges required, enter password for {os.getlogin()}: ")
        p = subprocess.Popen(f"echo {root_password} | sudo -Sn {cmd}", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             shell=True)
    wait_for_interrupt(p, platform)


def connect(config, ovpn_config: str):
    platform = sys.platform
    command = config["openvpn"]["path"][platform]

    if platform.startswith("win32"):
        connect_win(command, ovpn_config)

    elif platform.startswith("linux"):
        connect_posix(command, ovpn_config, platform)

    elif platform.startswith("darwin"):
        connect_posix(command, ovpn_config, platform)

    else:
        print(f"Unsupported platform: {platform}")
