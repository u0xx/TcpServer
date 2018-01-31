import socket
import socketserver
import time
from Message import Message

user_list = []


class TransSever(socketserver.BaseRequestHandler):
    times_out = 200
    user_now = {}
    data_size = -1

    def setup(self):
        print('-' * 40)
        self.request.settimeout(self.times_out)
        self.user_addr = "%s(%d)" % (self.client_address[0], self.client_address[1])
        print('connect from %s ' % self.user_addr)

    def handle(self):
        conn = self.request
        while True:
            try:
                recv_data = conn.recv(2048)
                if recv_data:
                    print('[client]%s:receved %d bytes' % (time.ctime(), len(recv_data)))
                    if 'msg_recv' in locals().keys() and msg_recv.is_part():
                        msg_recv.add_data(recv_data)
                    elif recv_data[3] > 0:
                        del msg_recv
                        continue
                    else:
                        msg_recv = Message(recv_data)

                    if msg_recv.is_part():
                        continue
                    else:
                        msg = msg_recv
                        del msg_recv

            except (socket.timeout, ConnectionAbortedError) as err:
                print('%s   %s' % (self.user_addr, err))
                break

            if msg:
                data_type = msg.typ
                user = msg.usr
                to_user = msg.to_usr

                if msg.typ > 0:
                    send_msg['data'] = 'command send failed'
                    for user_one in user_list:
                        if to_user == user_one['user']:
                            if user_one.__contains__('conn'):
                                user_one['conn'].sendall(data_all)
                                send_msg['data'] = 'command send success'
                            break
                    send_msg['cmd'] = 'info'
                    send_msg_byte = (repr(send_msg)).encode(encoding='utf-8')
                    send_msg_header = bytearray(6)
                    send_msg_all_byte = send_msg_header + user + to_user + send_msg_byte
                    conn.sendall(send_msg_all_byte)
                    print('transmit command  from %s to %s' % (user, to_user))

                else:
                    try:
                        msg_dic = msg.get_dic()
                    except NameError as err:
                        print(err)
                        continue
                    if msg_dic['cmd'] == 'conn':
                        find = False
                        user_now = {}
                        user_now['user'] = user
                        user_now['addr'] = self.client_address[0]
                        user_now['port'] = self.client_address[1]
                        for user_one in user_list:
                            if to_user == user_one['user']:
                                user_now['to_addr'] = user_one['addr']
                                user_now['to_port'] = user_one['port']
                                find = True
                                break
                        for user_one in user_list:
                            if user_now['user'] == user_one['user']:
                                user_list.remove(user_one)
                                break
                        msg_send = user_now.copy()
                        msg_send['cmd'] = 'conn'
                        msg_send['data'] = find
                        user_now['conn'] = self.request
                        self.user_now = user_now.copy()
                        user_list.append(self.user_now)

                        msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
                        send_msg_header = bytearray(6)
                        send_msg_all_byte = send_msg_header + user + to_user + msg_send_byte
                        conn.sendall(send_msg_all_byte)
                        print('%s is connect' % user_now['user'])


                    elif msg_dic['type'] == 'bye':
                        print('%s quit  ' % user)
                        break
                    elif msg_dic['cmd'] == 'keep':
                        msg_send = msg_dic.copy()
                        msg_send['data'] = 'link ok'
                        msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
                        send_msg_header = bytearray(6)
                        send_msg_all_byte = send_msg_header + user + to_user + send_msg_byte
                        conn.sendall(send_msg_all_byte)
                        print('%s alive  ' % user)

            time.sleep(0.5)

    def finish(self):
        print('%s from %s disconnect' % (self.user_addr, self.user_addr))
        if self.user_now:
            try:
                user_list.remove(self.user_now)
            finally:
                for user in user_list:
                    print('  %s' % user)
        print(' -' * 20)


def byte2int4(buf):
    return buf[0] + (buf[1] << 8) + (buf[2] << 16) + (buf[3] << 24)


def byte2int2(buf):
    return buf[0] + (buf[1] << 8)


if __name__ == '__main__':
    trans_server = socketserver.ThreadingTCPServer(('localhost', 12348), TransSever)
    print('server run ...')
    trans_server.serve_forever()
