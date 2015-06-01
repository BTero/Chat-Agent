from network import Handler, poll
from threading import Thread
from time import sleep
from PIL import Image
import sys

done = False
# displayed = False
im = Image.open("sam.png")

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                        
    
def options():
    # global displayed
    # displayed = True
    print("[1] Complaint\n[2] Question\n[3] Other\n[4] Quit \n")
    choice = int(raw_input("Choose one of the above:"))
    if choice == 1:
        print("Connecting to agent...")
        client.do_send("Client Option: complaint.")
        print("Connected")

    elif choice == 2:
        client.do_send("Client Option: question")
        userTopicInput = raw_input("Enter your topic: ")
        client.do_send((str(userTopicInput).split(' ')))
        print("Connecting to agent...")
        print("Connected")

    elif choice == 3:
        print("Connecting to agent...")
        client.do_send("Client Option: other")
        print("Connected")

    elif choice == 4:
        print("Quitting")
        client.do_close()
    else:
        print("You need to pick options 1, 2, 3 or 4")
        options()

transcript = []
def append_data_to_transcript(data):
    transcript.append('\n' + data)

def save_transcript():
    with open("transcript.txt", "wb") as text_file:
        for s in transcript:
            text_file.write(str(s))

def send_message(choiceInput):
    append_data_to_transcript(choiceInput)
    client.do_send(choiceInput)

def show_image():
    im.show()

class Client(Handler):
    in_chat = False

    def on_open(self):
        pass
        # print ('Client started')

    def on_close(self):
        global done
        done = True
        print ('Client closed')
        self.do_send('QUIT')

    def on_msg(self, data):
        if '!!QUIT!!' in data:
            global done
            done = True
            client.on_close()
        # if 'Choose one of the above:' in data:
        #     choice = int(raw_input())
        #     self.do_send('Client Option: ' + choice)
        append_data_to_transcript(data)
        print data

# ip = '68.5.75.43' # Yuki's host
portn = 8888
# ip = '169.234.104.169'
ip = 'localhost'
# ip = str(raw_input("Please enter the IP Address you would like to connect to: "))
# host, port = '192.168.0.19', 8888 #laptop host
# host, port = 'cs137.dtdns.net', 8888

host, port = ip, portn
client = Client(host, port)

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

options()
while not done:
    # if not check_wait_list():
    #     options()

    # choiceInput = raw_input('> ')
    choiceInput = sys.stdin.readline().rstrip()

    if ':q' in choiceInput:
        client.do_close()
        done = True
    elif ':s' in choiceInput:
        save_transcript()
    elif ':e' in choiceInput:
        show_image()
    else:
        choiceInput = 'Client: ' + choiceInput
        send_message(choiceInput)

client.do_close()# cleanup
sys.exit()
