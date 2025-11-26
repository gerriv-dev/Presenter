import socket
import subprocess


def check_wifi_connection(interface="wlan0"):
    finished_states = ["100", "10", "20"]
    state = None

    try:
        while state not in finished_states:
            result = subprocess.check_output(
                ["nmcli", "-t", "-f", "GENERAL.STATE", "device", "show", interface],
                stderr=subprocess.DEVNULL,
            ).decode()

            state = result.split(":")[1].split()[0]

        if state == "100":
            return True

    except Exception:
        pass

    return False


def check_internet_connection(timeout=5):
    targets = ["1.1.1.1", "8.8.8.8"]
    socket.setdefaulttimeout(timeout)

    for host in targets:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, 53))
                return True

        except Exception:
            continue

    return False


def check_connection():
    if check_wifi_connection():
        if check_internet_connection():
            return True

    return False
