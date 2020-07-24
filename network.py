import socket
import pickle
import time

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "35.228.23.197"
        #192.168.1.246 35.228.23.197
        self.port = 5555
        self.HEADERSIZE = 8
        self.addr = (self.server, self.port)
        self.client.connect(self.addr)
        self.RX_SIZE = 512
        self.init_info = self.receive()

    def send(self, data):
        msg = pickle.dumps(data)
        tx_msg = bytes(f'{len(msg):<{self.HEADERSIZE}}', "utf-8") + msg
        try:
            self.client.sendall(tx_msg)
        except socket.error as e:
            print(e)
            print("closing client socket...")
            self.client.close()

    def receive(self):

        receiving = True
        new_msg = True
        full_msg = b''
        buffer_size=self.RX_SIZE
        count = 0
        total_loop_num = -1
        tx_time = time.perf_counter()
        while receiving:
            if count == total_loop_num:
                buffer_size = rem_buffer_size

            msg = self.client.recv(buffer_size)
            print("ETR: ", time.perf_counter()-tx_time)
            tx_time = time.perf_counter()

            if new_msg:
                msg_len = int(msg[:self.HEADERSIZE])
                rem_buffer_size = (msg_len+self.HEADERSIZE) % self.RX_SIZE
                total_loop_num = (msg_len+self.HEADERSIZE) // self.RX_SIZE
                new_msg = False
                #print("msg length: ", msg_len)
                #print("rem_buffer_size:", rem_buffer_size)
                #print("total loop num",total_loop_num)

            full_msg += msg
            count += 1

            if len(full_msg)-self.HEADERSIZE == msg_len:
                receiving = False

        #print("ETR: ", post_tx_time-pre_tx_time)
        print("msg size: ", len(full_msg))
        data = full_msg[self.HEADERSIZE:]
        return data

    def close(self):
        self.client.close()

    #def connect(self):
        #self.client.connect(self.addr)
        #init_data = pickle.loads(self.client.recv(self.RX_SIZE))
        #print("initially received: ", init_data)
        #return self.client.recv(self.RX_SIZE).decode()
        #return init_data
