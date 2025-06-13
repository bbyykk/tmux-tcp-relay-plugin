#!/usr/bin/env python3
import socket
import threading
import argparse
import sys
import time
import signal
import os  # added for exit

class TcpRelay:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []

    def set_socket_options(self, sock):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def handle_client(self, conn, addr):
        print(f"[+] Client connected: {addr}")
        self.clients.append(conn)
        try:
            while True:
                data = conn.recv(65536)
                if not data:
                    print(f"[-] Client disconnected: {addr}")
                    break
                print(data.decode('utf-8'), end='', flush=True)
                for c in self.clients[:]:
                    if c is not conn:
                        try:
                            c.sendall(data)
                        except:
                            pass
        except Exception as e:
            print(f"[!] Error with {addr}: {e}")
        finally:
            if conn in self.clients:
                self.clients.remove(conn)
            conn.close()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"[i] Server listening on {self.host}:{self.port}")

        def shutdown_handler(sig, frame):
            print("[!] SIGINT received, shutting down")
            self.server_socket.close()
            sys.exit(0)
        signal.signal(signal.SIGINT, shutdown_handler)

        def local_input_loop():
            while True:
                try:
                    user_input = sys.stdin.readline()
                    if not user_input:
                        break
                    data = user_input.encode('utf-8')
                    for c in self.clients[:]:
                        try:
                            c.sendall(data)
                        except:
                            pass
                except Exception as e:
                    print(f"[!] Server input error: {e}")
                    break

        threading.Thread(target=local_input_loop, daemon=True).start()

        while True:
            try:
                conn, addr = self.server_socket.accept()
            except OSError:
                break
            self.set_socket_options(conn)
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def start_client(self, relay_host):
        def recv_thread(sock):
            try:
                while True:
                    data = sock.recv(65536)
                    if not data:
                        print("[!] Server closed connection")
                        os._exit(0)
                    print(data.decode('utf-8'), end='', flush=True)
            except Exception as e:
                print(f"[!] Receiving error: {e}")
                os._exit(0)

        def send_thread(sock):
            try:
                while True:
                    user_input = sys.stdin.readline()
                    if not user_input:
                        break
                    sock.sendall(user_input.encode('utf-8'))
            except Exception as e:
                print(f"[!] Sending error: {e}")
                os._exit(0)

        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((relay_host, self.port))
                self.set_socket_options(s)
                print(f"[i] Connected to relay at {relay_host}:{self.port}")

                recv_t = threading.Thread(target=recv_thread, args=(s,), daemon=True)
                send_t = threading.Thread(target=send_thread, args=(s,), daemon=True)
                recv_t.start()
                send_t.start()

                recv_t.join()
                send_t.join()
            except Exception as e:
                print(f"[!] Connection error: {e}")
                break
            finally:
                s.close()
            print("[!] Server is unreachable. Client exiting.")
            break

def main():
    parser = argparse.ArgumentParser(
        description="TCP relay utility (server/client)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'mode_or_host',
        nargs='?',
        default='server',
        help="Specify 'server' to start server, or use as relay host for client mode"
    )
    parser.add_argument('-p', '--port', type=int, default=5555, help="TCP port to use")
    args = parser.parse_args()

    relay = TcpRelay(port=args.port)

    if args.mode_or_host == 'server':
        relay.start_server()
    else:
        host = args.mode_or_host or 'localhost'
        relay.start_client(host)

if __name__ == "__main__":
    main()
