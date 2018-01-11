import socket
import socketserver
import time

user_list = []


class TransSever(socketserver.BaseRequestHandler):
    times_out = 20
    user_addr = ''
    user_now = {}
    user_to = {}

    def setup(self):
        print('-' * 40)
        #self.request.settimeout(self.times_out)
        self.user_addr = "%s(%d)" % (self.client_address[0], self.client_address[1])
        print('connect from %s ' % self.user_addr)

    def handle(self):
        conn = self.request
        while True:
            try:
                data_byte = conn.recv(2048)
                print('[client]%s:%s' % (time.ctime(), data_byte.decode()))
            except (socket.timeout, ConnectionAbortedError) as err:
                print('%s   %s' % (self.user_addr, err))
                break
            if data_byte:
                try:
                    data_dic = eval(data_byte)
                except NameError as err:
                    print(err)
                    conn.sendall(data_byte)
                    continue
                if data_dic['type'] == 'conn':
                    find = False
                    user_now = data_dic
                    user_now['addr'] = self.client_address[0]
                    user_now['port'] = self.client_address[1]
                    for user_one in user_list:
                        if user_now['to_user'] == user_one['user']:
                            user_now['to_addr'] = user_one['addr']
                            user_now['to_port'] = user_one['port']
                            self.user_to = user_one
                            find = True
                            break
                    for user_one in user_list:
                        if user_now['user'] == user_one['user']:
                            user_list.remove(user_one)
                            break

                    msg_send = user_now.copy()
                    del user_now['type']
                    self.user_now = user_now.copy()
                    self.user_now['conn'] = self.request
                    user_list.append(self.user_now)
                    if (find):
                        msg_send['suc'] = 1
                    else:
                        msg_send['suc'] = 0
                    msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
                    conn.sendall(msg_send_byte)
                    print('%s is connect' % user_now['user'])
                elif data_dic['type'] == 'exe':
                    msg_send = data_dic.copy()
                    msg_send['msg'] = 'target not online'
                    for user_one in user_list:
                        if data_dic['to_user'] == user_one['user']:
                            if user_one.__contains__('conn'):
                                user_one['conn'].sendall(data_byte)
                                msg_send['msg'] = 'command send success'
                            break
                    msg_send['type'] = 'info'
                    msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
                    conn.sendall(msg_send_byte)
                    print('transmit command  from %s to %s' % (data_dic['user'], data_dic['to_user']))
                elif data_dic['type'] == 'exec':
                    trans_result = 'false'
                    for user_one in user_list:
                        if data_dic['to_user'] == user_one['user']:
                            user_one['conn'].sendall(data_byte)
                            print('transmit result from %s to %s ' % (data_dic['user'], data_dic['to_user']))
                            trans_result = 'success'
                            break
                    print('transmit  result %s' % trans_result)
                elif data_dic['type'] == 'info':
                    trans_result = 'false'
                    for user_one in user_list:
                        if data_dic['to_user'] == user_one['user']:
                            user_one['conn'].sendall(data_byte)
                            trans_result = 'success'
                            print('transmit info from %s to %s  ' % (data_dic['user'], data_dic['to_user']))
                    print('transmit  result %s' % trans_result)
                elif data_dic['type'] == 'bye':
                    print('%s quit  ' % (data_dic['user']))
                    break
                elif data_dic['type'] == 'keep':
                    msg_send = data_dic.copy()
                    msg_send['msg'] = 'link ok'
                    msg_send_byte = (repr(msg_send)).encode(encoding='utf-8')
                    conn.sendall(msg_send_byte)
                    print('%s alive  ' % (data_dic['user']))

            time.sleep(0.1)

    def finish(self):
        print('%s from %s disconnect' % (self.user_addr, self.user_addr))
        if self.user_now:
            try:
                user_list.remove(self.user_now)
            finally:
                for user in user_list:
                    print('  %s' % user)
        print(' -' * 20)


if __name__ == '__main__':
    trans_server = socketserver.ThreadingTCPServer(('0.0.0.0', 12348), TransSever)
    print('server run ...')
    trans_server.serve_forever()