from network import Listener, Handler, poll, get_my_ip
import sys

done = False
clients = []

def broadcast(data):
    global clients
    print len(clients)

    for c in clients:
        c.do_send(data)

class MyHandler(Handler):
    
    def on_open(self):
        global clients
        if len(clients) < 2:
            clients.append(self)
        
    def on_close(self):
        global clients
        clients.remove(self)

    def on_msg(self, data):
        global clients
        if 'QUIT' in data:
            global done
            done = False
        else:
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
