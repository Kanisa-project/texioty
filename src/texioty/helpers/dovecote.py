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
DEFAULT_MESSAGE_PORT = 8020
DEFAULT_GAME_PORT = 8080
DOVECOT_LISTEN_PORT = 8210
DOVECOT_IP_PREFIX = "7.41.241"

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

def list_interfaces():
    """ Get list of interfaces except loopback."""
    base = '/sys/class/net/'
    try:
        return [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n))]
    except Exception as e:
        print(f"Error listing network interfaces: {e}")
        return []

def iface_ips(iface):
    try:
        out = subprocess.check_output(['ip', '-4', 'addr', 'show', 'dev', iface], text=True,
                                      stderr=subprocess.DEVNULL)
    except Exception as e:
        print(e)
        return []
    addrs = []
    for line in out.splitlines():
        line = line.strip()
        if 'inet ' in line:
            parts = line.split()
            if len(parts) >= 2:
                addrs.append(parts[1].split('/')[0])
    return addrs

# def get_linux_status():
#     status = {}
#     for iface in list_interfaces():
#         if iface == "lo":
#             continue
#         carrier = iface_carrier(iface)
#         oper = iface_operstate(iface)
#         ips = iface_ips(iface)
#         status[iface] = {'carrier': carrier, 'oper': oper, 'ips': ips}
#     return status

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
        self.socket = None
        self._create_socket()

        self.connected_pijuns: Dict[int, Dict[str, Any]] = {}
        self.message_board: List[Dict[str, Any]] = []
        self.game_sessions: Dict[str, Dict[str, Any]] = {}
        self.bound_iface: Optional[str] = None
        self.bound_address: Optional[tuple[str, int]] = None
        self.host_state_version = 0
        self.stale_timeout = 300.0

        self.watcher = NetworkWatcher(self.on_network_change, poll_interval=POLL_INTERVAL)
        self.watcher.start()

        self.receiver_thread = None
        self._running = False

        self.helper_commands = bind_commands(DOVECOT_COMMANDS, {
            "coop": self.start_dovecot,
            "decoop": self.stop_dovecot,
            "message": self.post_to_board
        })

    # def display_help_message(self, group_tag: Optional[str] = None):
    #     super().display_help_message(group_tag)

    def _create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(2.0)

    def reset_bindings(self):
        self.bound_iface = None
        self.bound_address = None
        self._running = False
        self.receiver_thread = None
        self.connected_pijuns.clear()
        self._update_hosting_header()

    def _update_hosting_header(self):
        if self._running and self.bound_address:
            host, port = self.bound_address
            iface_text = f" on {self.bound_iface}" if self.bound_iface else ""
            self.txo.update_header_status(
                right_status="HOSTING DOVECOT",
                bottom_status=f"{host}:{port}{iface_text}"
            )
        else:
            self.txo.update_header_status(
                right_status="",
                bottom_status=""
            )

    def start_dovecot(self, dovecot_num: str, gaim_engine: str = None):
        try:
            dovecot_num = int(dovecot_num)
        except ValueError:
            self.txo.priont_string("Invalid coop number. Please enter a number between 0 and 255.")
            return
        if dovecot_num < 0 or dovecot_num > 255:
            self.txo.priont_string("Invalid coop number. Please enter a number between 0 and 255.")
            return

        if self._running:
            self.stop_dovecot()

        if self.socket is None:
            self._create_socket()

        self.dovecot_id = dovecot_num
        target_ip = f"7.41.241.{dovecot_num}"
        address = (target_ip, 8080)
        iface = self._find_and_assign_ip(target_ip)
        if not iface:
            self.txo.priont_string(f"No IP address found for {target_ip}.")
            self.reset_bindings()
            return

        try:
            self.socket.bind(address)
            self.bound_iface = iface
            self.bound_address = address
            self.txo.priont_string(f"Dovecot server bound to {address}")
            self._running = True
            self.host_state_version += 1
            self._update_hosting_header()
            self.receiver_thread = threading.Thread(target=self._receive_pijuns, daemon=True)
            self.receiver_thread.start()
            self.txo.priont_string(f"Dovecot listening for pijuns on {address}")
            if gaim_engine:
                self.start_game_session(gaim_engine)
        except OSError as e:
            self.txo.priont_string(f"Error binding to {address}: {e}")
            if self.socket:
                self.socket.close()
                self.socket = None
            self._remove_assigned_ip(iface, target_ip)
            self.reset_bindings()
        except Exception as e:
            self.txo.priont_string(f"Error starting Dovecot server: {e}")
            if self.socket:
                self.socket.close()
                self.socket = None
            self._remove_assigned_ip(iface, target_ip)
            self.reset_bindings()

    def stop_dovecot(self):
        iface = self.bound_iface
        host = self.bound_address[0] if self.bound_address else None

        if not self._running and self.bound_address is None:
            self.reset_bindings()
            return

        old_socket = self.socket
        self.socket = None
        self._running = False

        if old_socket:
            try:
                old_socket.close()
            except Exception as e:
                self.txo.priont_string(f"Error closing socket: {e}")
        if iface and host:
            self._remove_assigned_ip(iface, host)
        self.reset_bindings()
        self._create_socket()
        self.txo.priont_string("Dovecot server stopped")

    def _receive_pijuns(self):
        self.txo.priont_string("Dovecot server is listening for pijuns/messages...")
        while self._running:
            self._cleanup_stale_pijuns()
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

    def _handle_pijun_payload(self, payload: Dict[str, Any], addr: tuple):
        payload_type = payload.get('type', 'unknown')
        pijun_id = payload.get('pijun_id', None)
        data = payload.get('data', '')
        request_id = payload.get('request_id')

        if payload_type == 'enter_coop':
            self._handle_enter_coop(pijun_id, data, addr, request_id)
            return
        if payload_type == 'heartbeat':
            self._handle_heartbeat(pijun_id, data, addr)
            return
        if payload_type == 'leave_coop':
            self._handle_leave_coop(pijun_id, data)
            return
        if payload_type == 'message':
            message_text = data.get('message', '') if isinstance(data, dict) else str(data)
            self._log_message(pijun_id, message_text, addr)
        elif payload_type == 'game_data':
            self._handle_game_data(pijun_id, data, addr)

        if pijun_id is not None:
            existing = self.connected_pijuns.get(pijun_id, {})
            self.connected_pijuns[pijun_id] = {
                'address': addr,
                'last_seen': time.time(),
                'type': payload_type,
                'session_id': existing.get('session_id'),
                'joined_at': existing.get('joined_at', time.time())
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
        if self._running and self.bound_iface and self.bound_iface in status:
            iface_info = status[self.bound_iface]
            ips = iface_info.get('ips', [])
            oper = iface_info.get('oper', 'unknown')
            host, port = self.bound_address if self.bound_address else ("?", self.port)
            ip_text = ", ".join(ips) if ips else host
            self.txo.update_header_status(
                right_status=f"HOSTING DOVECOT [{oper}]",
                bottom_status=f"{ip_text}:{port} on {self.bound_iface}"
            )

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
        self.stop_dovecot()
        if self.watcher:
            self.watcher.stop()
        if self.socket:
            self.socket.close()
            self.socket = None
        self.reset_bindings()
        self.txo.priont_string("Dovecot server stopped")

    def get_connected_pijuns(self) -> List[int]:
        return list(self.connected_pijuns.keys())

    def broadcast_message(self, message: str):
        payload = {
            'type': 'message',
            "protocol": 1,
            "timestamp": time.time(),
            "data": {
                "message": message
            }
        }
        pijun_ids_to_remove = []
        for pijun_id, info in self.connected_pijuns.items():
            try:
                self.socket.sendto(json.dumps(payload).encode('utf-8'), info['address'])
            except Exception as e:
                print(f"Error sending message to {pijun_id}: {e}")
                pijun_ids_to_remove.append(pijun_id)
        for pijun_id in pijun_ids_to_remove:
            self.connected_pijuns.pop(pijun_id, None)

    def _find_and_assign_ip(self, target_ip):
        interfaces = [iface for iface in list_interfaces() if iface != "lo"]

        def iface_priority(iface: str) -> tuple[int, str]:
            if iface.startswith(("enp", "eth")):
                return 0, iface
            elif iface.startswith(("wlan", "wlp")):
                return 1, iface
            return 2, iface

        interfaces.sort(key=iface_priority)

        for iface in interfaces:
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

    def _remove_assigned_ip(self, iface: str, target_ip: str):
        try:
            if target_ip not in iface_ips(iface):
                return
            subprocess.run(
                ["sudo", "ip", "addr", "del", f"{target_ip}/24", "dev", iface],
                check=True,
                capture_output=True,
                timeout=5
            )
            self.txo.priont_string(f"Removed IP {target_ip} from interface {iface}")
        except subprocess.CalledProcessError as e:
            self.txo.priont_string(f"Error removing IP {target_ip} from interface {iface}: {e}")
        except Exception as e:
            self.txo.priont_string(f"Error removing IP {target_ip} from interface {iface}: {e}")

    def _cleanup_stale_pijuns(self):
        now = time.time()
        stale_ids = [
            pijun_id
            for pijun_id, info in self.connected_pijuns.items()
            if now - info.get('last_seen', now) > self.stale_timeout
        ]
        for pijun_id in stale_ids:
            self.connected_pijuns.pop(pijun_id, None)
            self.host_state_version += 1
            self.txo.priont_string(f"Pijun {pijun_id} has been disconnected")

    def _handle_enter_coop(self, pijun_id: Optional[int], data: Dict[str, Any], addr: tuple, request_id: Optional[str]):
        if pijun_id is None:
            self._send_packet({
                "type": "enter_reject",
                "protocol": 1,
                "request_id": request_id,
                "pijun_id": -1,
                "timestamp": time.time(),
                "data": {
                    "accepted": False,
                    "reason_code": "invalid_request",
                    "reason": "Missing pijun_id."
                }
            }, addr)
            return

        existing = self.connected_pijuns.get(pijun_id)
        if existing and existing.get("address") != addr:
            self._send_packet({
                "type": "enter_reject",
                "protocol": 1,
                "request_id": request_id,
                "pijun_id": pijun_id,
                "timestamp": time.time(),
                "data": {
                    "accepted": False,
                    "reason_code": "duplicate_pijun_id",
                    "reason": "This pijun ID is already connected."
                }
            }, addr)
            return

        session_id = f"coop-{self.dovecot_id}-pijun-{pijun_id}"
        self.connected_pijuns[pijun_id] = {
            'address': addr,
            'last_seen': time.time(),
            'type': 'enter_coop',
            'session_id': session_id,
            'joined_at': time.time(),
            'client_name': data.get('client_name', f'Pijun {pijun_id}')
        }
        self._send_packet({
            "type": "enter_ack",
            "protocol": 1,
            "request_id": request_id,
            "pijun_id": pijun_id,
            "timestamp": time.time(),
            "data": {
                "accepted": True,
                "coop_id": self.dovecot_id,
                "session_id": session_id,
                "heartbeat_interval": 5.0,
                "host_state": self._build_host_state()
            }
        }, addr)
        self.txo.priont_string(f"Pijun {pijun_id} entered from {addr[0]}:{addr[1]}")

    def _handle_heartbeat(self, pijun_id: Optional[int], data: Dict[str, Any], addr: tuple):
        if pijun_id is None or pijun_id not in self.connected_pijuns:
            return
        self.connected_pijuns[pijun_id]['last_seen'] = time.time()
        self.connected_pijuns[pijun_id]['address'] = addr
        last_known_state_version = data.get('last_known_state_version', 0)
        if last_known_state_version < self.host_state_version:
            self._send_host_state(addr, pijun_id)
        self.txo.priont_string(f"Pijun {pijun_id} heartbeat from {addr[0]}:{addr[1]}")

    def _handle_leave_coop(self, pijun_id: Optional[int], data: Dict[str, Any]):
        if pijun_id is None:
            return
        removed = self.connected_pijuns.pop(pijun_id, None)
        if removed:
            self.host_state_version += 1
            self.txo.priont_string(f"Pijun {pijun_id} left")

    def _send_packet(self, packet: Dict[str, Any], addr: tuple):
        try:
            self.socket.sendto(json.dumps(packet).encode('utf-8'), addr)
        except Exception as e:
            print(f"Error sending packet to {addr[0]}:{addr[1]}: {e}")

    def _build_host_state(self) -> Dict[str, Any]:
        if self.game_sessions:
            game_name = next(iter(self.game_sessions))
            session = self.game_sessions[game_name]
            players = session.get('players', set())
            return {
                "coop_id": self.dovecot_id,
                "hosting_type": "game_session",
                "engine": game_name,
                "state": "active" if players else "waiting_for_players",
                "title": f"{game_name} Lobby",
                "player_count": len(players),
                "max_players": 4,
                "actions_allowed": ['chat', 'join_game', 'submit_guess'],
                "state_version": self.host_state_version
            }
        return {
            "coop_id": self.dovecot_id,
            "hosting_type": "message_board",
            "engine": None,
            "state": "idle",
            "title": "Message Board",
            "player_count": len(self.connected_pijuns),
            "max_players": 32,
            "actions_allowed": ['chat'],
            "state_version": self.host_state_version
        }

    def _send_host_state(self, addr, pijun_id):
        self._send_packet({
            "type": "host_state",
            "protocol": 1,
            "request_id": f"host-state-{pijun_id}-{int(time.time() * 1000)}",
        }, addr)
