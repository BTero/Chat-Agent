from network import Handler, poll
import threading
from threading import Thread
from time import sleep
import sys

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds

class Agent(Handler):

    def on_open(self):
        print ('Agent started')

    def on_close(self):
        global done
        done = True
        print ('Agent closed')
        self.do_send('QUIT')
        
    def on_msg(self, data):
        print data

done = False

# host, port = '68.5.75.43', 8888 # hosted by Yuki
host, port = 'localhost', 8888 # when server is hosted on same computer as Agent
agent = Agent(host, port)

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies
thread.start()
lock = threading.Lock()
agent.do_send('An agent has entered the chat.')

while not done:
    choiceInput = sys.stdin.readline().rstrip()
    if ':q' in choiceInput:
        agent.do_close()
        done = True
    else:
        choiceInput = 'Agent: ' + choiceInput
        agent.do_send(choiceInput)
agent.do_close() # cleanup
sys.exit()
