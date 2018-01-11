import socket

HOST = 'localhost'
PORT = 12348
BUFSIZ = 102400
local_id = 'ttt'
remote_id = 'rttt'
while (True):
    local_id = input('local id:')
    remote_id = input('romote id:')
    if not local_id or not remote_id or remote_id == local_id:
        print('input error,please try again')
        continue
    else:
        break

tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClient.connect((HOST, PORT))

# first conn
msg_send = {'type': 'conn', 'user': local_id, 'to_user': remote_id}
msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
tcpClient.sendall(msg_send_byte)
data_recv = tcpClient.recv(BUFSIZ)
print('[Server]%s ' % data_recv)
data_dic = eval(data_recv)
if data_dic['type'] == 'conn':
    if not data_dic['suc']:
        print('%s is not online' % remote_id)
    else:
        print('connect to %s success!' % remote_id)


while True:

    data = input('>>')
    send_message = {'type': 'info', 'user': local_id, 'to_user': remote_id, 'msg': data}
    byte_data = (repr(send_message)).encode(encoding='utf-8')
    if not data:
        break
    tcpClient.sendall(byte_data)
    data = tcpClient.recv(BUFSIZ)
    print(data)
    if not data:
        break
