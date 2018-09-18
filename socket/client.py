import socket               # 导入 socket 模块
import json
s = socket.socket()         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 10028                # 设置端口号

s.connect((host, port))
f = s.recv(1024)
f2 = f.decode()
print (f2)
s.close()