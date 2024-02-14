from network import Network
from support import timed_loop
import time, socket

# password = "owo"
network_manager = Network()
my_ip = network_manager.my_ip

print("searching for a host...")
network_manager.search = True
time.sleep(5)

print(f"ip addresses found: {network_manager.available_servers}")


if(not network_manager.available_servers):
    print("no hosts have been found..\nYou are the Host now")
    network_manager.search = False
    network_manager.broadcast = True
    # server code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        port = network_manager.port
        server.bind((my_ip, port))
        server.listen()
        while True: # this loop accepts connections and creates a thread for each connections the thread is handled in the network class
            client_socket, address = server.accept()
            network_manager.add_client(client_socket, address)



else:
    print(f"you will connect to {network_manager.available_servers[0]}...")
    # client code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        port = network_manager.port
        server_ip = network_manager.available_servers[0]
        client.connect((server_ip, port))
        print("connected successfully")
        while True:
            msg = input("send: ")
            client.sendall(msg.encode("utf-8"))
            data = client.recv(1024)
            print(data.decode('utf-8'))



network_manager.close()
