from network import Listener, Handler, poll, get_my_ip
import sys

done = False
clients = []
wait_list = []

def broadcast(data):
    global clients
    print len(clients)

    for c in clients:
        c.do_send(data)

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
        return default

class MyHandler(Handler):
    
    def on_open(self):
        global clients, wait_list
        if len(clients) < 2:
            clients.append(self)
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
            done = False
        else:
            if self in clients:
                broadcast(data)
                print(data)

port = 8888
server = Listener(port, MyHandler)
print ('Server started')
print 'Server IP Address: ' + str(get_my_ip())
while not done:
    poll(timeout=0.05)
server.stop()  # cleanup
sys.exit()
