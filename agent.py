from network import Handler, poll, poll_for


done = False

class Agent(Handler):
    
    def on_open(self):
        print ('Agent started')

    def on_close(self):
        print ('Agent closed')
        
    def on_msg(self, data):
        print data

        
host, port = 'localhost', 8888
agent = Agent(host, port)
while not done:
    poll(timeout=0.05)
    choiceInput = 'Agent:' + str(raw_input())
    agent.do_send(str(choiceInput))

agent.do_close() # cleanup
