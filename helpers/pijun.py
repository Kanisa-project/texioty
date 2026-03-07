import json
import os
import socket
import subprocess
import threading
import time
from typing import Optional, Any, Dict

from .registries.command_definitions import bind_commands, PIJUN_COMMANDS
# from texioty import texoty, texity
from .tex_helper import TexiotyHelper
# from settings import themery as t

POLL_INTERVAL = 1.0

def list_interfaces():
    base = '/sys/class/net/'
    try:
        return [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]
    except Exception as e:
        print(f"Error listing interfaces: {e}")
        return []

def read_file(path):
    try:
        # os.chmod(path, 0o666)
        with open(path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return None

def iface_carrier(iface):
    carrier = read_file(f'/sys/class/net/{iface}/carrier')
    return int(carrier) if carrier else None

def iface_operstate(iface):
    operstate = read_file(f'/sys/class/net/{iface}/operstate')
    return operstate.strip() if operstate else None

def iface_ips(iface):
    try:
        out = subprocess.check_output(['ip', '-4', 'addr', 'show', 'dev', iface], text=True,
                                      stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error getting IPs for {iface}: {e}")
        return []
    addrs = []
    for line in out.splitlines():
        line = line.strip()
        if 'inet ' in line:
            parts = line.split()
            if len(parts) >= 2:
                addrs.append(parts[1].split('/')[0])
    return addrs

def get_linux_status():
    status = {}
    for iface in list_interfaces():
        if iface == "lo":
            continue
        carrier = iface_carrier(iface)
        oper = iface_operstate(iface)
        ips = iface_ips(iface)
        status[iface] = {'carrier': carrier, 'oper': oper, 'ips': ips}
    return status

# def interpret_state(info):
#     carrier = info.get('carrier')
#     oper = info.get('oper')
#     ips = info.get('ips', [])
#     if carrier is False or (oper and oper.lower() in ("down", "no-carrier")):
#         return "no_link", "Cable unplugged"
#     if carrier is True:
#         if ips:
#             return "connected_with_ip", f"Connected with IP {', '.join(ips)}"
#         return "cabled_detected_no_ip", "Cable detected (no IP)"
#     if oper and oper.lower() in ("up", "unknown", "dormant", "lowerlayerdown"):
#         if ips:
#             return "connected_with_ip", f"Connected with IP {', '.join(ips)}"
#         return "connected_no_ip", f"Operstate={oper} (no IP)"
#     if ips:
#         return "connected_with_ip", f"Has IP {', '.join(ips)}"
#     return "unknown", "Unknown"

# class CoopWatcher(threading.Thread):
#     """
#     Listen for ethernet connections and trigger callbacks when changes occur.
#     """
#     def __init__(self, callback, poll_interval=POLL_INTERVAL):
#         super().__init__(daemon=True)
#         self.callback = callback
#         self.poll_interval = poll_interval
#         self._stop = threading.Event()
#         self.last = {}
#
#     def run(self):
#         while not self._stop.is_set():
#             # print('CoopWatcher running.')
#             try:
#                 raw = get_linux_status()
#                 interp = {}
#                 for iface, info in raw.items():
#                     code, text = interpret_state(info)
#                     interp[iface] = {"code": code, "text": text}
#                     # print(interp[iface])
#                 if interp != self.last:
#                     self.callback(interp)
#                     self.last = interp
#             except Exception as e:
#                 self.callback({"__error__": {"code": "unknown", "text": str(e)}})
#                 print(f"Error in CoopWatcher: {e}")
#             time.sleep(self.poll_interval)
#
#     def stop(self):
#         self._stop.set()


class Pijun(TexiotyHelper):
    def __init__(self, txo, txi, pijun_id: int = 0):
        """
        Allows for other devices to send a pijun to a coop server.
        """
        super().__init__(txo, txi)
        self.pijun_id = pijun_id
        self.buff_size = 2048
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = 2.0
        self.socket.settimeout(self.timeout)
        self.helper_commands = bind_commands(PIJUN_COMMANDS, {
            "send": self.send_message,
            "deliver": self.send_game_data
        })

    def display_help_message(self, group_tag: Optional[str] = None):
        super().display_help_message(group_tag)

    def send_message(self, message: str, host: str, port: str):
        if not message or not message.strip():
            self.txo.priont_string("No message provided.")
            return
        try:
            port = int(port)
        except ValueError:
            port = 8020
            self.txo.priont_string("Invalid port number. Using default port 8020.")
        if port < 1 or port > 65535:
            self.txo.priont_string("Invalid port number. Must be between 1 and 65535.")
            return

        address = (host, port)
        payload = {
            "type": "message",
            "pijun_id": self.pijun_id,
            "data": message
        }

        try:
            self.socket.sendto(json.dumps(payload).encode('utf-8'), address)
            self.txo.priont_string(f"Message sent to {host}:{port}")
            print(f"Message sent: {message[:50]}...")
        except socket.gaierror as e:
            self.txo.priont_string(f"Error resolving host: {e}")
            print(f"Error resolving host: {e}")
        except OSError as e:
            self.txo.priont_string(f"Network error sending to {host}:{port}: {e}")
        except Exception as e:
            self.txo.priont_string(f"Error sending message: {e}")
            print(f"Error sending message: {e}")

    def send_game_data(self, game_data: str, host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            port = 8080
            self.txo.priont_string("Invalid port number. Using default port 8080.")
        if port < 1 or port > 65535:
            self.txo.priont_string("Invalid port number. Must be between 1 and 65535.")
            return

        address = (host, port)
        try:
            parsed = json.loads(game_data)
        except json.JSONDecodeError as e:
            self.txo.priont_string(f"Error parsing game data: {e}")
            return

        payload = {
            "type": "game_data",
            "pijun_id": self.pijun_id,
            "data": parsed
        }

        try:
            self.socket.sendto(json.dumps(payload).encode('utf-8'), address)
            self.txo.priont_string(f"Game data sent to {host}:{port}")
        except socket.gaierror as e:
            self.txo.priont_string(f"Error resolving host: {e}")
        except OSError as e:
            self.txo.priont_string(f"Network error sending to {host}:{port}: {e}")
        except Exception as e:
            self.txo.priont_string(f"Error sending game data: {e}")
            print(f"Error sending game data: {e}")

    def send_raw(self, payload: Dict[str, Any], host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            self.txo.priont_string("Invalid port number. Using default port 8020.")
            return False

        if port < 1 or port > 65535:
            self.txo.priont_string("Invalid port number. Must be between 1 and 65535.")
            return False
        address = (host, port)
        try:
            self.socket.sendto(json.dumps(payload).encode('utf-8'), address)
            self.txo.priont_string(f"Raw data sent to {host}:{port}")
            return True
        except socket.gaierror as e:
            self.txo.priont_string(f"Error resolving host: {e}")
            print(f"Error resolving host: {e}")
            return False
        except OSError as e:
            self.txo.priont_string(f"Network error sending to {host}:{port}: {e}")
        except Exception as e:
            self.txo.priont_string(f"Error sending raw data: {e}")
            print(f"Error sending raw data: {e}")
            return False

