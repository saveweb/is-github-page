import socket
import os
import urllib.request
num = 1


githubip = urllib.request.urlopen('https://api.github.com/meta')
githubip = str(githubip.read())

os.system("wget https://github.com/timqian/chinese-independent-blogs/raw/master/blogs-original.csv -O ./blogs-original.csv")

with open('blogs-original.csv', 'r') as f:
  lines = f.read()
  lines = lines.splitlines()
with open('gh-domains.txt', 'w') as f:
  for line in lines[1:]:
    print(num)
    num = num + 1
    line = line.replace(" ", "").split(',')
    domain = line[1].replace("https://", "").replace("http://", "").replace("/", "")
    try:
      ip = socket.gethostbyname(domain)
      ip = ip.split('.')
      ip_head = ip[0]+'.'+ip[1]+'.'+ip[2]
      isfind = githubip.find(ip_head)
      if isfind != -1 :
        f.write(domain+"\n")
        print(domain+"is on GH-page!")
    except:
      continue