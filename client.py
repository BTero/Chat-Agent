from network import Handler, poll
from threading import Thread
from time import sleep
import sys

done = False

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                        
    
def options():
    print("[1] Complaint\n[2] Question\n[3] Other\n")
    choice = int(raw_input("Choose one of the above:"))
    if choice == 1:
        print("Connecting to agent...")
        client.do_send("Client: complaint.")

    elif choice == 2:
        client.do_send("Client: question")
        userTopicInput = raw_input("Enter your topic: ")
        client.do_send((str(userTopicInput).split(' ')))
        print("Connecting to agent...")

    elif choice == 3:
        print("Connecting to agent...")
        client.do_send("Client: other")

    else:
        print("You need to pick options 1, 2, or 3!")
        options()

transcript = []
def append_data_to_transcript(data):
    transcript.append('\n' + data)

def save_transcript():
    with open("transcript.txt", "wb") as text_file:
        for s in transcript:
            text_file.write(str(s))

class Client(Handler):
    def on_open(self):
        print ('Client started')
        client.do_send('A client has entered the chat.')
        # options()

    def on_close(self):
        print ('Client closed')

    def on_msg(self, data):
        append_data_to_transcript(data)
        print data


host, port = '192.168.0.19', 8888
client = Client(host, port)

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while not done:
    choiceInput = sys.stdin.readline().rstrip()

    if ':q' in choiceInput:
        client.do_close()
    elif ':s' in choiceInput:
        save_transcript()
    else:
        choiceInput = 'Client: ' + choiceInput
        client.do_send(choiceInput)

client.do_close()# cleanup
