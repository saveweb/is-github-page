import socket
import urllib.request
import urllib.parse

try:
  githubip = urllib.request.urlopen('https://api.github.com/meta')
  githubip = str(githubip.read())
except:
  print('无法访问GitHub-API，请检查网络。')
else:
    print('请输入域名/链接')
    line = input()
    line = line.replace(" ", "")
    res = urllib.parse.urlparse(line)
    domain = res.netloc
    try:
      ip = socket.gethostbyname(domain)
      ip = ip.split('.')
      ip_head = ip[0]+'.'+ip[1]+'.'+ip[2]
      isfind = githubip.find(ip_head)
      if isfind != -1 :
        print(domain+" 是GH-Pages!")
      else:
        print(domain+" 不是GH-Pages!")
    except:
      print('错误: DNS无法解析或其它问题。')