import socket
import threading
import time
import logging
import sys


logging.basicConfig(level=logging.DEBUG) # use logging.debug() instead of print in threads

def get_myip():   # this is stupid i should find another way
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ip = None  # Define local_ip here
    try:
    # Doesn't even have to be reachable
        s.connect(("10.0.0.1", 80))  #"10.0.0.1" is often used as a default gateway for routers
        local_ip = s.getsockname()[0]
        print(f"Local IP address is {local_ip}")
    except Exception as e:
        print("Error:", e)
    finally:
        s.close()
        return local_ip



class Network:
    # this class has methods that help manage the networking of the game
    def __init__(self):
        self.port = 1313
        self.password = 'owo'
        self.my_ip = get_myip()


        # client variables
        self.search = False
        self.available_servers = []
        self.clients = []
        self.search_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.search_socket.bind(('', self.port))

        # server variables
        self.broadcast_address = ('255.255.255.255', self.port)
        self.broadcast = False
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # enables broadcasting

        # enabling the threads
        self.search_thread = threading.Thread(target=self.search_for_ips)
        self.search_thread.daemon = True  # Set as daemon thread   |  means the thread will be closed when the program is exited
        self.search_thread.start()

        self.broadcast_thread = threading.Thread(target=self.broadcast_password)
        self.broadcast_thread.daemon = True  # Set as daemon thread
        self.broadcast_thread.start()



    # client methods
    def search_for_ips(self):         # this should be run in another thread
        # listens to the broadcast
        while True:
            if self.search:
                data, address = self.search_socket.recvfrom(1024)
                # logging.debug(f'data:{data}, address {address}')
                if data.decode() == 'owo' and not address[0] in self.available_servers:
                    self.available_servers.append(address[0])
                    #  print(f'a new server ip have been found!! it is : {address[0]}, data : {data}')
                    # NOTE : i must write something to check if the server is disconnected and remove it from the list if so
                    # maybe a refresh button that just emptys the servers list
                    # i will leave this task for the client_handler method

    # server methods
    def broadcast_password(self):      # this should be run in another thread
        # sends a password over the broadcast ip address
        while True:
            if self.broadcast:
                self.broadcast_socket.sendto(self.password.encode(), self.broadcast_address)
                #logging.debug(f"Broadcasting password: {self.password}")
                time.sleep(1)

    def close(self):
        self.search_socket.close()
        self.broadcast_socket.close()
        for socket, ip in self.clients:
            socket.close()
            print(f"closed connection with {ip}")


    def client_handler(self, conn, address): # runs in another thread to handle the interactions between each client
        while True:
            try:
                data = conn.recv(1024)
                msg = data.decode('utf-8')
                if(not data or msg == "-quit"):
                    print("connection closed by client.")
                    self.clients.remove([conn, address])
                    conn.close()
                    for c in self.clients:
                        print(f"clients: {c[1]}")
                    break
                # print(f"server recived: {data.decode('utf-8')}")
                    # send the msg to all the clients except the one who sent it
                for socket, addr in self.clients:
                    print(f"addr: {addr}  address: {address}")
                    if addr != address:
                        socket.sendall((address+": "+msg).encode('utf-8'))
                    else:
                        socket.sendall("(sent)".encode("utf_8"))
            except Exception as e:
                print(f"Error: {e}")
                break

    def add_client(self, client_socket, address):
        self.clients.append([client_socket, address])
        # print(f"{address} hava joined the chat !")
        thread = threading.Thread(target=self.client_handler, args=(client_socket, address))
        thread.daemon = True
        thread.start()



# network = Network()
# print(f'my ip address is {network.my_ip}')
