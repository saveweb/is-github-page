import socket
import os
import urllib.parse
num = 1

try:
  os.system("wget https://github.com/timqian/chinese-independent-blogs/raw/master/blogs-original.csv -O ./blogs-original.csv")
  with open('blogs-original.csv', 'r') as f:
   lines = f.read()
except:
  print("您似乎没有安装wget，请手动下载文件 https://github.com/timqian/chinese-independent-blogs/raw/master/blogs-original.csv 并放至当前目录")
else:
  with open('blogs-original.csv', 'r') as f:
    lines = f.read()
    lines = lines.splitlines()
  with open('gh-domains.txt', 'w') as f:
    for line in lines[1:]:
      print(num)
      num = num + 1
      line = line.replace(" ", "").split(',')
      res = urllib.parse.urlparse(line[1])
      domain = res.netloc
      try:
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
      except:
        continue

os.system("rm blogs-original.csv -rf")