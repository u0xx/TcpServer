import socket

HOST = 'test.xcan.cn'
PORT = 12348
BUFSIZ = 102400
local_id = 'ttt'
remote_id = 'ttt'
while(True):
    local_id=input('local id:')
    remote_id=input('romote id:')
    if not local_id or not remote_id or remote_id==local_id:
        print('input error,please try again')
        continue
    else:
        break



tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcpClient.connect((HOST, PORT))
tcpClient.connect(('localhost', PORT))

#first conn
msg_send = {'type':'conn','user':local_id,'to_user':remote_id}
msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
tcpClient.sendall(msg_send_byte)
data_recv = tcpClient.recv(BUFSIZ)
print('[Server]%s ' % data_recv)
data_dic = eval(data_recv)
if data_dic['type'] == 'conn':
    if not data_dic['suc']:
        print('connect failed!')
        exit(0)
    else:
        print('connect to server sucsess!')

#register self
msg_send = {'type': 'reg', 'user': local_id}
msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
tcpClient.sendall(msg_send_byte)
data_recv = tcpClient.recv(BUFSIZ)
print('[Server]%s ' % data_recv)
data_dic = eval(data_recv)
if data_dic['type'] == 'reg':
    if not data_dic['suc']:
        print('connect failed!')
        exit(0)
    else:
        print('register to server sucsess!')

#find rometo user
msg_send = {'type': 'find', 'user': local_id,'to_user':remote_id}
msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
tcpClient.sendall(msg_send_byte)
data_recv = tcpClient.recv(BUFSIZ)
print('[Server]%s ' % data_recv)
data_dic = eval(data_recv)
if data_dic['type'] == 'find':
    if not data_dic['suc']:
        print('find %s failed!'%remote_id)
    else:
        print('find %s sucsess!'%remote_id)
        print('-' * 80)
        print(data_dic['msg'])

while True:


    data = input('>>')
    send_message = {'type': 'reg', 'user': local_id, 'msg': data}
    byte_data = (repr(send_message)).encode(encoding='utf-8')
    if not data:
        break
    tcpClient.sendall(byte_data)
    data = tcpClient.recv(BUFSIZ)
    print(data)
    if not data:
        break
