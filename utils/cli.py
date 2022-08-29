import time

from fabric import Connection
from paramiko.ssh_exception import NoValidConnectionsError


def stabilize_connection(c: Connection, max_retries: int, sleep_seconds: int):
    attempt = 0
    while attempt < max_retries:
        try:
            c.run("echo Connected!")
            break
        except NoValidConnectionsError:
            print(f"Attempt failed ({attempt}/{max_retries}")
            attempt += 1
            time.sleep(sleep_seconds)
            print("Trying again...")
