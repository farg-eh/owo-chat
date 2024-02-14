import time


# a while loop that keeps executing a function for a period of time
def timed_loop(seconds, func):
    start = time.time()
    while(time.time() - start < seconds):
        func()

def client_handler(self, conn, address):
    while True:
        try:
            data = conn.recv(1024)
            msg = data.decode('utf-8')
            if not data or msg == "-quit":
                print("Connection closed by client.")
                self.clients.remove([conn, address])
                conn.close()
                for c in self.clients:
                    print(f"Clients: {c[1]}")
                break

            # Send the message to all clients except the one who sent it
            for socket, addr in self.clients:
                if addr != address:
                    socket.sendall((address + ": " + msg).encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break
