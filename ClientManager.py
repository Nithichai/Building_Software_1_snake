import socket

class ClientManager():
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def set_pattern(self, index, ls_data):
        packet  = str(index) + ","
        for ls in ls_data:
            packet += str(ls) + ","
        return packet[:-1]
    
    def send(self, data):
        print "CLIENT SEND:" + data
        self.sock.sendto(data, (self.host, self.port))
    
    def recv(self):
        packet, addr = self.sock.recvfrom(1024)
        print "CLIENT  RECV:" + packet
        return packet, addr
    
    def close(self):
        self.sock.close()
    
    def split(self, packet):
        list_recv = []
        ls_1d = packet.split("/")
        for i in range(len(ls_1d)):
            list_recv.append([])
            ls_2d = ls_1d[i].split(",")
            for ls in ls_2d:
                list_recv[i].append(ls)
        return list_recv
    
    def pos_split(self, pos):
        new_pos = pos.split("|")
        new_pos = [int(new_pos[i]) for i in range(len(new_pos))]
        return new_pos
    
    def pos_pattern(self, list_pos):
        packet = ""
        for ls in list_pos:
            packet += str(ls) + "|"
        return packet[:-1]