import os
import socket
import subprocess
import threading
import time
from typing import Optional

from texioty import texoty, texity
from .tex_helper import TexiotyHelper
from settings import themery as t

POLL_INTERVAL = 1.0

FULL_HELP = {
    "coop": {"usage": "'coop [0-255] [GAIM_ENGINE]'",
             "arg_desc": {"coop": "A coop server can host a gaim.",
                          "[0-255]": "The \"coop number\", so pijuns can join and play.",
                          "[GAIM_ENGINE]": "Gaim engine to run in the coop server."},
             "examples": ["coop 0 trailin", "coop 132 slinger", "coop 67 thurbo", "coop 255 k_paint"]
             },
    "pijun": {"usage": "'pijun [0-255] [enter/leave] (0-255)'",
              "arg_desc": {"pijun": "A pijun acts as a player in a coop server.",
                           "[0-255]": "A number to assign to a pijun entering a coop.",
                           "[enter/leave]": "Enter or leave a coop server.",
                           "(0-255)": "Only needed if entering a coop."},
              "examples": ["pijun 241 enter 41", "pijun 147 leave", "pijun 16 enter 213"]
              },
    # "enter": {"usage": "'enter [0-255]'",
    #           "arg_desc": {"enter": "Enter a coop server to play a gaim.",
    #                        "[0-255]": "The \"coop number\" to join."},
    #           "examples": ["enter 132", "enter 2", "enter 67"]
    #           },
    # "leave": {"usage": "'leave'",
    #           "arg_desc": ["Leave a coop server."],
    #           "examples": ["leave"]
    #           },
}

def list_interfaces():
    base = '/sys/class/net/'
    try:
        return [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]
    except Exception as e:
        return []

def read_file(path):
    try:
        # os.chmod(path, 0o666)
        with open(path, 'r') as f:
            return f.read().strip()
    except Exception:
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
    except Exception:
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

def interpret_state(info):
    carrier = info.get('carrier')
    oper = info.get('oper')
    ips = info.get('ips', [])
    if carrier is False or (oper and oper.lower() in ("down", "no-carrier")):
        return "no_link", "Cable unplugged"
    if carrier is True:
        if ips:
            return "connected_with_ip", f"Connected with IP {', '.join(ips)}"
        return "cabled_detected_no_ip", "Cable detected (no IP)"
    if oper and oper.lower() in ("up", "unknown", "dormant", "lowerlayerdown"):
        if ips:
            return "connected_with_ip", f"Connected with IP {', '.join(ips)}"
        return "connected_no_ip", f"Operstate={oper} (no IP)"
    if ips:
        return "connected_with_ip", f"Has IP {', '.join(ips)}"
    return "unknown", "Unknown"

class CoopWatcher(threading.Thread):
    def __init__(self, callback, poll_interval=POLL_INTERVAL):
        super().__init__(daemon=True)
        self.callback = callback
        self.poll_interval = poll_interval
        self._stop = threading.Event()
        self.last = {}

    def run(self):
        while not self._stop.is_set():
            print('CoopWatcher running.')
            try:
                raw = get_linux_status()
                interp = {}
                for iface, info in raw.items():
                    code, text = interpret_state(info)
                    interp[iface] = {"code": code, "text": text}
                    # print(interp[iface])
                if interp != self.last:
                    self.callback(interp)
                    self.last = interp
            except Exception as e:
                self.callback({"__error__": {"code": "unknown", "text": str(e)}})
                print(f"Error in CoopWatcher: {e}")
            time.sleep(self.poll_interval)

    def stop(self):
        self._stop.set()


class PijunCooper(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY, host='127.0.0.1', port=8008):
        super().__init__(txo, txi)
        self.buff_size = 1024
        self.pijun_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.coop_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.coop_address = ("7.41.241.42", 8080)
        self.pijun_address = ("4.20.60.9", 8020)
        self.pijuns = {}
        self.pijun_addresses = {}
        self.watcher = CoopWatcher(self.on_pijun_change, poll_interval=POLL_INTERVAL)
        # self.watcher.start()
        self.helper_commands['coop'] = {"name": "coop",
                                        "usage": "'coop [0-255] [GAIM_ENGINE]'",
                                        "call_func": self.host_dovecot,
                                        "lite_desc": "Host a coop server for pijuns.",
                                        "full_desc": ["Host a coop server for pijuns to play and poop in."],
                                        "possible_args": {},
                                        "args_desc": {'[0-255]': ['The coop number.', int],
                                                      '[GAIM_ENGINE]': ['The gaim engine to run in the coop.', str]},
                                        'examples': ['coop 42 trailin', 'coop 84 slinger'],
                                        "group_tag": "PIJN",
                                        "font_color": t.rgb_to_hex(t.PIGEON_GREY),
                                        "back_color": t.rgb_to_hex(t.BLACK)}
        self.helper_commands['pijun'] = {"name": "pijun",
                                         "usage": "'pijun [0-255] [enter/leave] (0-255)'",
                                         "call_func": self.send_pijun,
                                         "lite_desc": "Send a pijun to a coop server.",
                                         "full_desc": ["Find a pijun to send.", "(0-255) is only for entering a coop."],
                                         "possible_args": {},
                                         "args_desc": {'[0-255]': ['The pijun number.', int],
                                                       '[enter/leave]': ['Enter or leave a coop.', str],
                                                       '(0-255)': ['The coop number to join.', int]},
                                         'examples': ['pijun 74 enter 42', 'pijun 121 leave'],
                                         "group_tag": "PIJN",
                                         "font_color": t.rgb_to_hex(t.PIGEON_GREY),
                                         "back_color": t.rgb_to_hex(t.BLACK)}

    def display_help_message(self, group_tag: Optional[str] = None):
        super().display_help_message(group_tag)

    def enter_dovecot(self, host: str, port: str):
        print(f"trying to enter to {host} {port}")
        self.coop_socket.bind((host, int(port)))
        self.txo.priont_string(f"coop socket bound to {host}:{port}")
        coop_thread = threading.Thread(target=self.coop_receive_data)
        coop_thread.start()
        self.txo.priont_string("coop_thread_started")

    def leave_dovecot(self, host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            port = 8008
        address = (host, port)
        self.coop_socket.sendto(bytes("Goodbye, I am leaving.", "utf-8"), address)
        self.unassign_ip("enp4s0")
        self.coop_socket.close()
        self.txo.priont_string(f"coop socket sent goodbye to {address}")

    def send_pijun(self, host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            port = 8008
        address = (host, port)
        self.pijun_socket.sendto(bytes(f"Hello, I am {self.pijun_address} pijun.", "utf-8"), address)

    def coop_receive_data(self):
        while True:
            data, addr = self.coop_socket.recvfrom(self.buff_size)
            if not data:
                break
            self.txo.priont_string(data.decode())
            self.txo.priont_string(f"...received from {addr}")
            print(data.decode())

    def on_pijun_change(self, status):
        print("Status", status)
        for iface in sorted(status.keys()):
            info = status[iface]
            code = info.get('code', "unknown")
            text = info.get('text', "")
            if "(no IP)" in text:
                # self.texoty.priont_string("No IP detected")
                self.assign_ip(iface)
            self.txo.priont_string(f"{iface}: {code} {text}")

    def assign_ip(self, iface):
        """Assign an IP address to a given interface."""
        try:
            subprocess.run(["sudo", "ip", "addr", "add", self.coop_address[0], "dev", iface], check=True)
            self.txo.priont_string(f"{self.coop_address[0]} assigned to {iface}")
        except Exception as e:
            print(f"Error assigning {self.coop_address[0]}: {e}")

    def unassign_ip(self, iface):
        try:
            subprocess.run(["sudo", "ip", "addr", "del", self.coop_address, "dev", iface], check=True)
            self.txo.priont_string(f"{self.coop_address} unassigned from {iface}")
        except Exception as e:
            print(f"Error unassigning {self.coop_address}: {e}")

    def host_dovecot(self, coop_num: str, gaim_engine: str):
        address = (f"7.41.241.{coop_num}", 8080)
        print(f"trying to bind to {address}")
        self.txo.priont_string(f"coop socket bound to {address} for playing {gaim_engine}")
        self.txo.priont_string("coop_thread_started")


    def start_slinger_coop(self):
        self.txo.master.gaim_registry.start_game('slinger')

    # def host_dovecot(self, host: str, port: str):
    #     try:
    #         port = int(port)
    #     except ValueError:
    #         port = 8008
    #     address = (host, port)
    #     print(f"trying to bind to {address}")
    #     self.coop_socket.bind(address)
    #     self.txo.priont_string(f"coop socket bound to {address}")
    #     coop_thread = threading.Thread(target=self.coop_receive_data)
    #     coop_thread.start()
    #     self.txo.priont_string("coop_thread_started")
