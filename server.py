from network import Listener, Handler, poll


done = False
clients = []

def broadcast(data):
    global clients
    print len(clients)

    for c in clients:
        c.do_send(data)

class MyHandler(Handler):
    
    def on_open(self):
        print ('server open')
        
    def on_close(self):
        print ('server closed')
        global done
        done = True;

    def on_msg(self, data):
        global clients
        if self not in clients:
            clients.append(self)

        broadcast(data)
        print(data)

port = 8888
server = Listener(port, MyHandler)
print ('Server started')
while not done:
    poll(timeout=0.05)
server.stop()  # cleanup
