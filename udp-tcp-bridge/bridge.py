import socket
import sys
from thread import *
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port

robot_message = "none"

joy_left_x = 0.0
joy_left_y = 0.0
joy_right_x = 0.0
joy_right_y = 0.0
message_left = 'left'
message_right = 'right'
message_joy = 'joy'

heart_rate = 0.0
message_heart = 'heart'
message_rate = 'rate'

message_req = 'req'
message_rep = 'rep'



 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    start_new_thread(udpClientThread ,(conn,))
    #Sending message to connected client
###    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'ref ' + str(0.123) + " " + str(0.456)
        print reply
        if not data: 
            break
        
        ds = data.split(" ")
        if len(ds) > 0:
          if ds[0] == message_req:
            if ds[1] == message_joy:
              if len(ds) >= 3:
                if ds[2] == message_left:
                  sendJoystick(conn, message_left, joy_left_x, joy_left_y)
                if ds[2] == message_right:
                  sendJoystick(conn, message_right, joy_right_x, joy_right_y)
                  
        ##conn.sendall(robot_message)
        #conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client


def sendJoystick(conn, stick, x, y):
  reply = message_rep + ' ' + message_joy + ' ' + stick + ' ' + str(x) + ' ' + str(y)
  conn.sendall(reply)

def udpClientThread(conn):
  global robot_message
  global joy_left_x
  global joy_left_y
  global joy_right_x
  global joy_right_y
  global heart_rate
  
  
  
  
  robot_message = "no"
  UDP_IP = "104.131.47.73"
  UDP_PORT = 2362

  sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))
  print "in udp thread"
  while True:
      data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
      robot_message = data
      ds = data.split(" ")
      if ds[0] == message_heart:
        if ds[1] == message_rate:
          if len(ds) >= 3:
            heart_rate = float(ds[2])
      if ds[0] == message_joy:
          if len(ds) >= 4:
            if ds[1] == message_left:
              joy_left_x = float(ds[2])
              joy_left_y = float(ds[3])
            if ds[1] == message_right:
              joy_right_x = float(ds[2])
              joy_right_y = float(ds[3])              
      print "received message:", data
      

while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
