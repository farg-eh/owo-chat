from network import Network
from support import timed_loop
import time, socket, threading

# password = "owo"
name = input("Enter a nickname: ")
network_manager = Network()
my_ip = network_manager.my_ip

def become_server():
    # print("no hosts have been found..\nYou are the Host now")
    network_manager.search = False
    network_manager.broadcast = True
    # server code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        port = network_manager.port
        server.bind((my_ip, port))
        server.listen()
        while network_manager.running: # this loop accepts connections and creates a thread for each connections the thread is handled in the network class
            client_socket, address = server.accept()
            client_name = client_socket.recv(1024).decode("utf-8")
            network_manager.add_client(client_socket, address[0], client_name)
    sys.exit()


print("searching for a host...")
network_manager.search = True
time.sleep(5)

print(f"ip addresses found: {network_manager.available_servers}")


if(not network_manager.available_servers):  # if there is not host broadcasting your password
    thread = threading.Thread(target=become_server)
    thread.daemon = True
    thread.start()
    host_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(1)
    host_client.connect((my_ip, network_manager.port))
    host_client.sendall(name.encode("utf-8"))

    while network_manager.running:
        data = host_client.recv(1024)
        print(data.decode('utf-8'))
        msg = input("send: ")
        host_client.sendall(msg.encode("utf-8"))





else:
    print(f"you will connect to {network_manager.available_servers[0]}...")
    # client code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        port = network_manager.port
        server_ip = network_manager.available_servers[0]
        client.connect((server_ip, port))
        print("connected successfully")
        client.sendall(name.encode("utf-8"))
        while network_manager.running:
            data = client.recv(1024)
            print(data.decode('utf-8'))
            msg = input("send: ")
            client.sendall(msg.encode("utf-8"))




network_manager.close()
