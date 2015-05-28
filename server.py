from network import Listener, Handler, poll


done = False
clients = []

class MyHandler(Handler):
    
    def on_open(self):
        print ('server open')
        
    def on_close(self):
        print ('server closed')
        global done
        done = True;

    def on_msg(self, data):
        print(data)
        # global clients
        # for c in clients:
        #     c.do_send(data)

    @staticmethod
    def on_accept(self, h):
        print 'hello'
        global clients
        if len(clients) < 2:
            h.do_send("Welcome to the chat.")
            clients.append(h)
        else:
            h.do_send("Agent is currently busy. Please wait for your turn.")

port = 8888
server = Listener(port, MyHandler)
print ('Server started')
while not done:
    poll(timeout=0.05)
server.stop()  # cleanup
