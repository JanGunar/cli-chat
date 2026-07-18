import argparse
import socket
import threading

parser = argparse.ArgumentParser()
parser.add_argument("--listen", action="store_true")
parser.add_argument("--connect", metavar="IP")
parser.add_argument("--port", type=int, default=5000)
args = parser.parse_args()

connected = False

def get_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if args.listen:
        HOST = "0.0.0.0"
        PORT = args.port

        global connected

        s.bind((HOST,PORT))
        s.listen(1)

        conn, addr = s.accept()
        connected = True

        return conn
    if args.connect:
        HOST = args.connect
        PORT = args.port

        global connected 

        s.connect((HOST,PORT))
        connected = True

        return s

def receive_message(conn):
    global connected 

    while True:
        data = conn.recv(1024)
        if not data:
            print("No connection. Press ENTER to exit.")
            conn.close()
            connected = False
            break
        else:
            print(f"u2>{data.decode()}")

conn = get_connection()

thread = threading.Thread(target=receive_message, args=(conn,), daemon=True)
thread.start()

while connected:
    text_message = input("")
    if not connected: break
    else:
        if text_message in ("/q", "/quit", "/exit"):
            print("You left.")
            conn.close()
            break   
        else:
            conn.sendall(text_message.encode())


