import socket
import os

print('Please input domain:)
domain = input()
target_host = domain
target_port = 80
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host,target_port))
request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
client.send(request.encode())
response = client.recv(4096)  
http_response = repr(response)
http_response_len = len(http_response)
if str(response).find('Server: GitHub.com') != -1 :
  f.write(domain+"\n")
  print(domain+" is on GH-Pages!")