

from socket import *
import time
import threading


c = 0
complete = False

    
def send_requests(clientSocket):
    
    global c, complete
    offset = 0
    while c <= no_requests:
        clientSocket.sendto(f"Offset: {offset}\nNumBytes: 1448\n\n".encode(),(serverName, serverPort))
        offset += 1448
        if c <= no_requests:
            time.sleep(5)
    complete = True
            
def receive_messages(clientSocket):
    global c, complete, received_data
    
    while not complete:
        while True:
            #clientSocket.settimeout(0.01)
            try:
                reply, serverAddress = clientSocket.recvfrom(2048)
                decoded_data = reply.decode() 
                offset_line = decoded_data.split('\n')[0]
                data_list = decoded_data.split('\n', 3)
                
                o = int(offset_line.split(': ')[1])
                index = o//1448
                received_data[index] = data_list[3]
                c += 1
                print(c)
                
                break
            except timeout:
                print("TIMEOUT")
                break
            except:
                print('Connection lost from server')
                break
    
    
def main():
    
    global c, complete, sleep, received_data
    
    serverName = "127.0.0.1"
    serverPort = 9801

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = "SendSize\n\n"
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    reply, serverAddress = clientSocket.recvfrom(2048)
    r = reply.decode()
    print(r)
    #clientSocket.close()
    size_string = r.split(":")[1].strip()
    size = int(size_string)

    no_requests = (size//1448)+1
    
    received_data = [""]*no_requests
    
    receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
    receive_thread.start()
    
    offset = 0
    i = 0
    while i < no_requests:
        clientSocket.sendto(f"Offset: {offset}\nNumBytes: 1448\n\n".encode(),(serverName, serverPort))
        i += 1
        offset += 1448
        
        time.sleep(1)
        
    if c == i:
        complete = True
    else:
        to_receive = []
        for j in range(no_requests):
            if received_data[j] == "":
                to_receive.append(j)
    clientSocket.close()
    print(received_data)
       
    
main()

