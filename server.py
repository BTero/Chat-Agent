from network import Listener, Handler, poll, get_my_ip
import sys

done = False
clients = []
wait_list = []

def broadcast(self, data):
    global clients

    for c in clients:
        if self != c:
            c.do_send(data)

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
        return default

def get_wait_list():
    global wait_list
    return wait_list

# def check_wait_list(client):
#     global wait_list
#     return any(client == w for w in wait_list)

# def display_options(client):
#     client.do_send('[1] Complaint\n[2] Question\n[3] Other\nChoose one of the above:')

class MyHandler(Handler):

    def on_open(self):
        global clients, wait_list
        print len(clients)
        if len(clients) < 2:
            clients.append(self)
            # display_options(self)
        else:
            self.do_send("Agent is currently busy. Please wait until the Agent is available.")
            wait_list.append(self)
        
    def on_close(self):
        global clients
        global wait_list
        clients.remove(self)
        if wait_list:
            w = get_first(wait_list)
            w.do_send("You are now speaking with the Agent.")
            clients.append(w)
            wait_list.remove(w)

    def on_msg(self, data):
        global clients
        if 'QUIT' in data:
            global done
            done = True
        else:
            if self in clients:
                broadcast(self, data)
                print(data)

def main():
    port = 8888
    server = Listener(port, MyHandler)
    print ('Server started')
    print 'Server IP Address: ' + str(get_my_ip())
    while not done:
        poll(timeout=0.05)
    server.stop()  # cleanup
    sys.exit()

if __name__ == "__main__":
    main()
