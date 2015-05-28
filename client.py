from network import Handler, poll


done = False

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

transcript = ''
def append_data_to_transcript(data):
    transcript.append('\n' + data)

def save_transcript():
     with open("transcript.txt", "w") as text_file:
            text_file.write(transcript)

class Client(Handler):
    def on_open(self):
        print ('Client started')
        options()

    def on_close(self):
        print ('client closed')

    def on_msg(self, data):
        append_data_to_transcript(data)
        print data
        
host, port = 'localhost', 8888
client = Client(host, port)

while not done:
    poll(timeout=0.05)
    choiceInput = str(raw_input())
    if ':q' in choiceInput:
        client.do_close()
    elif ':s' in choiceInput:
        client.saveTranscript()
    else:
        choiceInput = 'Client:' + str(raw_input())
        client.do_send(str(choiceInput))

client.do_close()# cleanup
