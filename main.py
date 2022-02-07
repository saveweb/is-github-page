import socket
import urllib.request
import urllib.parse
num = 1

try:
  githubip = urllib.request.urlopen('https://api.github.com/meta')
  githubip = str(githubip.read())
except:
  print('无法访问GitHub-API，请检查网络。')

try:
  lines = urllib.request.urlopen('https://github.com/timqian/chinese-independent-blogs/raw/master/blogs-original.csv')
  lines = str(lines.read())
except:
  print("")
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
        ip = socket.gethostbyname(domain)
        ip = ip.split('.')
        ip_head = ip[0]+'.'+ip[1]+'.'+ip[2]
        isfind = githubip.find(ip_head)
        if isfind != -1 :
          f.write(domain+"\n")
          print(domain+" 是GH-Pages!")
      except:
        continue
