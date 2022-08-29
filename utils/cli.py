import subprocess


def run(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while process.stdout.readable():
        line = process.stdout.readline()

        if not line:
            break

        print(line.strip())
