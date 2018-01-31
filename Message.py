class Message:

    def __init__(self, data_byte):
        self.len = data_byte[0] + (data_byte[1] << 8) + (data_byte[2] << 16) + (data_byte[3] << 24)
        self.typ = data_byte[4] + (data_byte[5] << 8)
        self.usr = data_byte[6:14]
        self.to_usr = data_byte[14: 22]
        self.msg_byte = data_byte[22:]

    def add_data(self, add_byte):
        self.msg_byte = self.msg_byte + add_byte

    def is_part(self):
        return self.len > len(self.msg_byte)+22

    def get_dic(self):
        return eval(self.msg_byte)
