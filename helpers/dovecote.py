import os
import socket
import subprocess
import threading
import time
import json
from typing import Optional, Dict, List, Any

from .registries.command_definitions import bind_commands, DOVECOT_COMMANDS
from .tex_helper import TexiotyHelper

POLL_INTERVAL = 1.0
MESSAGE_BUFFER_SIZE = 100

class NetworkWatcher(threading.Thread):
    def __init__(self, callback, poll_interval=POLL_INTERVAL):
        super().__init__(daemon=True)
        self.callback = callback
        self.poll_interval = poll_interval
        self._stop = threading.Event()
        self.last = {}

    def run(self):
        while not self._stop.is_set():
            try:
                raw = self._get_linux_status()
                if raw != self.last:
                    self.callback(raw)
                    self.last = raw
            except Exception as e:
                print(f"Error in NetworkWatcher: {e}")
            time.sleep(self.poll_interval)

    def stop(self):
        self._stop.set()

    @staticmethod
    def _get_linux_status() -> Dict[str, Dict[str, Any]]:
        base = '/sys/class/net/'
        status = {}
        try:
            interfaces = [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]
            for iface in interfaces:
                if iface == "lo":
                    continue
                carrier = NetworkWatcher._read_carrier(iface)
                oper = NetworkWatcher._read_operstate(iface)
                ips = NetworkWatcher._read_ips(iface)
                status[iface] = {'carrier': carrier, 'oper': oper, 'ips': ips}
        except Exception as e:
            print(f"Error reading network status: {e}")
            pass
        return status

    @staticmethod
    def _read_carrier(iface: str) -> Optional[int]:
        try:
            with open(f'/sys/class/net/{iface}/carrier', 'r') as f:
                return int(f.read().strip())
        except Exception as e:
            print(f"Error reading carrier for {iface}: {e}")
            return None

    @staticmethod
    def _read_operstate(iface: str) -> Optional[str]:
        try:
            with open(f'/sys/class/net/{iface}/operstate', 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading operstate for {iface}: {e}")
            return None

    @staticmethod
    def _read_ips(iface: str) -> List[str]:
        try:
            out = subprocess.check_output(['ip', '-4', 'addr', 'show', 'dev', iface],
                                          text=True, stderr=subprocess.DEVNULL)
            addrs = []
            for line in out.splitlines():
                if 'inet ' in line:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        addrs.append(parts[1].split('/')[0])
            return addrs
        except Exception as e:
            print(f"Error reading IPs for {iface}: {e}")
            return []

# FULL_HELP = {
#     "coop": {"usage": "'coop [0-255] [GAIM_ENGINE]'",
#              "arg_desc": {"coop": "A coop server can host a gaim.",
#                           "[0-255]": "The \"coop number\", so pijuns can join and play.",
#                           "[GAIM_ENGINE]": "Gaim engine to run in the coop server."},
#              "examples": ["coop 0 trailin", "coop 132 slinger", "coop 67 thurbo", "coop 255 k_paint"]
#              },
#     "pijun": {"usage": "'pijun [0-255] [enter/leave] (0-255)'",
#               "arg_desc": {"pijun": "A pijun acts as a player in a coop server.",
#                            "[0-255]": "A number to assign to a pijun entering a coop.",
#                            "[enter/leave]": "Enter or leave a coop server.",
#                            "(0-255)": "Only needed if entering a coop."},
#               "examples": ["pijun 241 enter 41", "pijun 147 leave", "pijun 16 enter 213"]
#               },
    # "enter": {"usage": "'enter [0-255]'",
    #           "arg_desc": {"enter": "Enter a coop server to play a gaim.",
    #                        "[0-255]": "The \"coop number\" to join."},
    #           "examples": ["enter 132", "enter 2", "enter 67"]
    #           },
    # "leave": {"usage": "'leave'",
    #           "arg_desc": ["Leave a coop server."],
    #           "examples": ["leave"]
    #           },
# }

def list_interfaces():
    base = '/sys/class/net/'
    try:
        return [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]
    except Exception as e:
        print(f"Error listing network interfaces: {e}")
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


class Dovecot(TexiotyHelper):
    def __init__(self, txo, txi, dovecot_id: int = 0, host: str = '0.0.0.0', port: int = 8210):
        """
        Allows for other devices to send a pijun to a coop server.
        """
        super().__init__(txo, txi)
        self.dovecot_id = dovecot_id
        self.host = host
        self.port = port
        self.buff_size = 2048
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(2.0)

        self.connected_pijuns: Dict[int, Dict[str, Any]] = {}
        self.message_board: List[Dict[str, Any]] = []
        self.game_sessions: Dict[str, Dict[str, Any]] = {}

        self.watcher = NetworkWatcher(self.on_network_change, poll_interval=POLL_INTERVAL)
        self.watcher.start()

        self.receiver_thread = None
        self._running = False

        self.helper_commands = bind_commands(DOVECOT_COMMANDS, {
            "host": self.start_dovecot,
            "message": self.post_to_board
        })

    def display_help_message(self, group_tag: Optional[str] = None):
        super().display_help_message(group_tag)

    def start_dovecot(self, dovecot_num: str, gaim_engine: str = None):
        try:
            dovecot_num = int(dovecot_num)
        except ValueError:
            self.txo.priont_string("Invalid coop number. Please enter a number between 0 and 255.")
            return
        if dovecot_num < 0 or dovecot_num > 255:
            self.txo.priont_string("Invalid coop number. Please enter a number between 0 and 255.")
            return

        self.dovecot_id = dovecot_num
        target_ip = f"7.41.241.{dovecot_num}"
        address = (target_ip, 8080)
        iface = self._find_and_assign_ip(target_ip)
        if not iface:
            self.txo.priont_string(f"No IP address found for {target_ip}.")
            return

        try:
            self.socket.bind(address)
            self.txo.priont_string(f"Dovecot server bound to {address}")
            self._running = True
            self.receiver_thread = threading.Thread(target=self._receive_pijuns, daemon=True)
            self.receiver_thread.start()
            self.txo.priont_string(f"Dovecot listening for pijuns on {address}")
            if gaim_engine:
                self.start_game_session(gaim_engine)
        except OSError as e:
            self.txo.priont_string(f"Error binding to {address}: {e}")
            self._running = False
        except Exception as e:
            self.txo.priont_string(f"Error starting Dovecot server: {e}")
            self._running = False

    def _receive_pijuns(self):
        self.txo.priont_string("Dovecot server is listening for pijuns/messages...")
        while self._running:
            try:
                data, addr = self.socket.recvfrom(self.buff_size)
                if not data:
                    continue
                try:
                    payload = json.loads(data.decode('utf-8'))
                    self._handle_pijun_payload(payload, addr)
                except json.JSONDecodeError:
                    self.txo.priont_string(f"Received invalid JSON: {data.decode('utf-8')}")
                    self._handle_raw_message(data.decode('utf-8', errors='ignore'), addr)
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    self.txo.priont_string(f"Error receiving pijun: {e}")
                    print(f"Error receiving pijun: {e}")

    def _handle_pijun_payload(self, payload: Dict[str, Any], addr: tuple):
        payload_type = payload.get('type', 'unknown')
        pijun_id = payload.get('pijun_id', None)
        data = payload.get('data', '')

        if payload_type == 'message':
            self._log_message(pijun_id, data, addr)
        elif payload_type == 'game_data':
            self._handle_game_data(pijun_id, data, addr)

        if pijun_id is not None:
            self.connected_pijuns[pijun_id] = {
                'address': addr,
                'last_seen': time.time(),
                'type': payload_type
            }

    def _handle_raw_message(self, data: str, addr: tuple):
        self._log_message(None, data, addr)

    def _log_message(self, pijun_id: Optional[int], data: str, addr: tuple):
        entry = {
            'timestamp': time.time(),
            'pijun_id': pijun_id,
            'source': addr,
            'message': data,
        }
        self.message_board.append(entry)
        if len(self.message_board) > MESSAGE_BUFFER_SIZE:
            self.message_board.pop(0)
        source_label = f"Pijun {pijun_id}" if pijun_id is not None else f"Client {addr[0]}"
        self.txo.priont_string(f"[{source_label}]: {data}")

    def _handle_game_data(self, pijun_id: Optional[int], data: Dict[str, Any], addr: tuple):
        self.txo.priont_string(f"Game data from {pijun_id}: " )
        self.txo.priont_dict(data)
        if 'game' in data:
            game_name = data['game']
            if game_name in self.game_sessions:
                self.game_sessions[game_name]['last_update'] = time.time()
                self.game_sessions[game_name]['players'].add(pijun_id)

    def on_network_change(self, status: Dict[str, Dict[str, Any]]):
        for iface, info in status.items():
            ips = info.get('ips', [])
            oper = info.get('oper', 'unknown')
            if ips:
                self.txo.priont_string(f"Interface {iface} has IPs: {', '.join(ips)}")
    def post_to_board(self, message: str):
        entry = {
            'timestamp': time.time(),
            'pijun_id': None,
            'source': 'server',
            'message': message
        }
        self.message_board.append(entry)
        if len(self.message_board) > MESSAGE_BUFFER_SIZE:
            self.message_board.pop(0)
        self.txo.priont_string(f"Server: {entry}")

    def start_game_session(self, gaim_engine: str):
        session = {
            'engine': gaim_engine,
            'started': time.time(),
            'players': set(),
            'state': {}
        }
        self.game_sessions[gaim_engine] = session
        self.txo.priont_string(f"Started game session, {gaim_engine}:")
        self.txo.priont_dict(session)

    def add_player_to_session(self, gaim_engine: str, player_id: str):
        if gaim_engine not in self.game_sessions:
            self.txo.priont_string(f"Game session {gaim_engine} not found")
            return
        session = self.game_sessions[gaim_engine]
        session['players'].add(player_id)
        self.txo.priont_string(f"Added player {player_id} to session {gaim_engine}")
        self.txo.priont_dict(session)

        if hasattr(self.txo, 'master') and hasattr(self.txo.master, 'gaim_registry'):
            self.txo.master.gaim_registry.start_game(gaim_engine, player_id)

    def stop(self):
        self._running = False
        if self.watcher:
            self.watcher.stop()
        if self.socket:
            self.socket.close()
        self.txo.priont_string("Dovecot server stopped")

    def get_connected_pijuns(self) -> List[int]:
        return list(self.connected_pijuns.keys())

    def broadcast_message(self, message: str):
        payload = {
            'type': 'message',
            'message': message
        }
        for pijun_id, info in self.connected_pijuns.items():
            try:
                self.socket.sendto(json.dumps(payload).encode('utf-8'), info['address'])
            except Exception as e:
                print(f"Error sending message to {pijun_id}: {e}")
                self.connected_pijuns.pop(pijun_id)

    def _find_and_assign_ip(self, target_ip):
        interfaces = list_interfaces()
        for iface in interfaces:
            if iface == "lo":
                continue
            try:
                subprocess.run(
                    ["sudo", "ip", "addr", "add", f"{target_ip}/24", "dev", iface],
                    check=True,
                    capture_output=True,
                    timeout=5
                )
                self.txo.priont_string(f"Assigned IP {target_ip} to interface {iface}")
                return iface
            except subprocess.CalledProcessError as e:
                if "File exists" not in str(e.stderr):
                    self.txo.priont_string(f"Error assigning IP {target_ip} to interface {iface}: {e}")
                else:
                    self.txo.priont_string(f"IP {target_ip} already assigned to interface {iface}")
                    return iface
                continue
            except Exception as e:
                print(f"Error assigning IP {target_ip} to interface {iface}: {e}")
                continue
        return None
