import json
import os
import socket
import subprocess
import threading
import time
from typing import Optional, Any, Dict

from .registries.command_definitions import bind_commands, PIJUN_COMMANDS
from .tex_helper import TexiotyHelper

POLL_INTERVAL = 1.0

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

        self.connected_coop: Optional[Dict[str, Any]] = None
        self.host_state: Optional[Dict[str, Any]] = None
        self._running = True
        self._joined = False
        self._pending_requests: Dict[str, Dict[str, Any]] = {}
        self._pending_lock = threading.Lock()

        self._listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listener_thread.start()
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()

        self.helper_commands = bind_commands(PIJUN_COMMANDS, {
            "send": self.send_message,
            "deliver": self.send_game_data,
            "enter": self.enter_coop,
            "leave": self.leave_coop,
        })

    def display_help_message(self, group_tag: Optional[str] = None):
        super().display_help_message(group_tag)

    def _make_request_id(self, prefix: str) -> str:
        return f"{prefix}-{self.pijun_id}-{int(time.time() * 1000)}"

    def _build_payload(self, payload_type: str, data: Dict[str, Any], request_id: Optional[str] = None) -> Dict[str, Any]:
        return {
            "type": payload_type,
            "protocol": 1,
            "request_id": request_id or self._make_request_id(payload_type),
            "pijun_id": self.pijun_id,
            "timestamp": time.time(),
            "data": data
        }

    def _send_payload(self, payload: Dict[str, Any], host: str, port: int) -> bool:
        address = (host, port)
        try:
            self.socket.sendto(json.dumps(payload).encode('utf-8'), address)
            return True
        except socket.gaierror as e:
            self.txo.priont_string(f"Error resolving host: {e}")
            return False
        except OSError as e:
            self.txo.priont_string(f"Network error sending to {host}:{port}: {e}")
            return False
        except Exception as e:
            self.txo.priont_string(f"Error sending payload: {e}")
            return False

    def _register_pending_request(self, request_id: str) -> threading.Event:
        event = threading.Event()
        with self._pending_lock:
            self._pending_requests[request_id] = {
                "event": event,
                "response": None
            }
        return event

    def _resolve_pending_request(self, request_id: str, payload: Dict[str, Any]) -> bool:
        with self._pending_lock:
            pending = self._pending_requests.get(request_id)
            if not pending:
                return False
            pending["response"] = payload
            pending["event"].set()
            return True

    def _pop_pending_response(self, request_id: str) -> Optional[Dict[str, Any]]:
        with self._pending_lock:
            pending = self._pending_requests.pop(request_id, None)
        if not pending:
            return None
        return pending.get("response")

    def enter_coop(self, host: str, port: str = "8080", client_name: Optional[str] = None) -> bool:
        try:
            port = int(port)
        except ValueError:
            port = 8080
            self.txo.priont_string("Invalid port number. Using default port 8080.")
        if port < 1 or port > 65535:
            self.txo.priont_string("Invalid port number. Must be between 1 and 65535.")
            return False

        request_id = self._make_request_id("enter")
        wait_event = self._register_pending_request(request_id)
        payload = self._build_payload("enter_coop", {
            "client_name": client_name or f"Pijun {self.pijun_id}",
            "wants_host_state": True
        }, request_id=request_id)

        try:
            for _ in range(3):
                if not self._send_payload(payload, host, port):
                    continue
                if wait_event.wait(self.timeout):
                    break
                wait_event.clear()
            response = self._pop_pending_response(request_id)
            if not response:
                self.txo.priont_string(f"Timed out entering coop at {host}:{port}")
                return False
            response_type = response.get('type')
            response_data = response.get('data', {})
            if response_type == 'enter_ack':
                self.connected_coop = {
                    "host": host,
                    "port": port,
                    "coop_id": response_data.get('coop_id'),
                    "session_id": response_data.get('session_id'),
                    "heartbeat_interval": response_data.get('heartbeat_interval', 5.0),
                    "last_seen": time.time()
                }
                self.host_state = response_data.get('host_state')
                self._joined = True
                self.txo.priont_string(f"Successfully joined coop server at {host}:{port}")
                if self.host_state:
                    self._apply_host_state(self.host_state)
                return True

            if response_type == 'enter_reject':
                reason = response_data.get('reason', 'Join rejected')
                self.txo.priont_string(f"Failed to join coop server: {reason}")
                return False

            self.txo.priont_string(f"Unexpected response type: {response_type}")
            return False

        finally:
            with self._pending_lock:
                self._pending_requests.pop(request_id, None)


    def leave_coop(self, reason: str = "user_exit"):
        if not self.connected_coop:
            self.txo.priont_string("Not currently connected to a coop server.")
            return

        payload = self._build_payload("leave", {
            "session_id": self.connected_coop.get("session_id"),
            "reason": reason
        })
        self._send_payload(payload, self.connected_coop.get("host"), self.connected_coop.get("port"))
        self.connected_coop = None
        self.host_state = None
        self._joined = False
        self.txo.priont_string("Successfully left coop server.")

    def _listen_loop(self):
        while self._running:
            try:
                data, addr = self.socket.recvfrom(self.buff_size)
                if not data:
                    continue
                try:
                    payload = json.loads(data.decode('utf-8'))
                    self._handle_server_payload(payload, addr)
                except json.JSONDecodeError:
                    self.txo.priont_string(f"Received invalid JSON: {data.decode('utf-8')}")
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    self.txo.priont_string(f"Error processing packet: {e}")

    def _heartbeat_loop(self):
        while self._running:
            if self._joined and self.connected_coop:
                payload = self._build_payload("heartbeat", {
                    "session_id": self.connected_coop.get("session_id"),
                    "last_known_state_version": (self.host_state or {}).get("state_version", 0)
                })
                self._send_payload(payload, self.connected_coop.get("host"), self.connected_coop.get("port"))
            interval = 5.0
            if self.connected_coop:
                interval = self.connected_coop.get("heartbeat_interval", 5.0)
            time.sleep(interval)

    def _handle_server_payload(self, payload: Dict[str, Any], addr: tuple):
        payload_type = payload.get('type')
        data = payload.get('data', {})

        if payload_type == 'host_state':
            self.host_state = data
            if self.connected_coop:
                self.connected_coop['last_seen'] = time.time()
            self._apply_host_state(data)
        elif payload_type == 'enter_ack':
            self.host_state = data.get('host_state')
            if self.host_state:
                self._apply_host_state(self.host_state)
        elif payload_type == 'enter_reject':
            reason = data.get('reason', 'Join rejected')
            self.txo.priont_string(f"Failed to join coop server: {reason}")
        elif payload_type == 'message':
            message = data.get('data', '')
            self.txo.priont_string(f"[Coop]: {message}")


    def _apply_host_state(self, state: Dict[str, Any]):
        hosting_type = state.get('hosting_type', 'idle')
        engine = state.get("engine")
        title = state.get("title", "Coop")

        self.txo.priont_string(f"Hosting: {hosting_type} ({title})")
        if engine:
            self.txo.priont_string(f"Engine: {engine}")


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
