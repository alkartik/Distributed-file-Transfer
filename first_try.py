

from socket import *
import time

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

c = 1
offset = 0
sleep = 2
while c <= no_requests:
    #print(f"Data {c}")
    clientSocket.sendto(f"Offset: {offset}\nNumBytes: 1448\n\n".encode(),(serverName, serverPort))
    
    while True:
        clientSocket.settimeout(0.01)
        try:
            reply, serverAddress = clientSocket.recvfrom(2048)
            print(c)
            c += 1
            offset += 1448
            break
        except timeout:
            print("TIMEOUT")
            break
        except:
            print('Connection lost from server')
            break
    #print(reply.decode())

    
    if c <= no_requests:
        time.sleep(sleep)
    
clientSocket.close()    
    
    
    
    
    
    
    
    

