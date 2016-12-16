import socket
import time
import random
from TileManager import TileManager
from Database import Database
from Apple import Apple
from CounterTime import CounterTime

class Server():
    
    def __init__(self, host, port, user, pwd, db_name, tb_name):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db_name = db_name
        self.tb_name = tb_name
    
        self.max_player = 3
        self.server_state_dict = {'OK':0, 'notNStart':1, 'notNExit':2}
        self.server_state = self.server_state_dict['notNStart']
        self.play_state = False
        
        self.db_save_size = 6
        self.id = 0
        self.type = 1
        self.x = 2
        self.y = 3
        self.s = 4
        self.t = 5
        
        self.counter = CounterTime()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        print("Server start...")
        
        self.db = Database("localhost", self.user, self.pwd)
        self.db.create_db(self.db_name)
        self.db.create_tb(self.tb_name)
        print("Database start....")
        
    def recv(self):
        packet, self.addr = self.sock.recvfrom(1024)
        if packet.find("tile:") != -1:
            first_index = packet.find(":") + 1
            new_packet = packet[first_index:]
            ls = new_packet.split(",")
            self.tile_mng = TileManager(int(ls[0]), int(ls[1]), int(ls[2]), int(ls[3]))
            self.apple_x = random.randrange(0, self.tile_mng.get_nw_tile())
            self.apple_y = random.randrange(0, self.tile_mng.get_nh_tile())
            self.db.insert_data(self.tb_name, "*", "a", self.apple_x, self.apple_y, 0, 0)
        elif packet == "eaten" :
            self.apple_x = random.randrange(0, self.tile_mng.get_nw_tile())
            self.apple_y = random.randrange(0, self.tile_mng.get_nh_tile())
            self.db.insert_data(self.tb_name, "*", "a", self.apple_x, self.apple_y, 0, 0)
        elif packet == "pause" :
            self.counter.pause()
        elif packet == "stop" :
            self.counter.stop()
        else :
            ls_client = packet.split(",")
            self.db.insert_data(self.tb_name,
                                ls_client[self.id],
                                ls_client[self.type],
                                ls_client[self.x],
                                ls_client[self.y],
                                ls_client[self.s],
                                int(self.counter.get_time()))
    
    def send(self):
        packet = ""
        if self.server_state == self.server_state_dict['notNStart']:
            packet = "notNStart"
        elif self.server_state == self.server_state_dict['notNExit']:
            packet = "notNExit"
        else :
            ls_data = self.db.get_data(self.tb_name)
            packet = "*,a," + str(self.apple_x) + "," + str(self.apple_y) + ",0,0/"
            for ls in ls_data:
                for i in range(self.db_save_size-1):
                    packet += str(ls[i]) + ","
                packet += str(int(self.counter.get_time()))
                packet += "/"
            packet = packet[:-1]
        self.sock.sendto(packet, self.addr)
    
    def update(self):
        if len(self.db.get_data(self.tb_name)) >= self.max_player and not self.play_state :
            self.server_state = self.server_state_dict['OK']
            self.play_state = True
            self.counter.restart()
        elif len(self.db.get_data(self.tb_name)) < self.max_player and self.play_state :
            self.server_state = self.server_state_dict['notNExit']
            self.play_state = False
            self.counter.stop()
        elif len(self.db.get_data(self.tb_name)) < self.max_player and not self.play_state :
            self.server_state = self.server_state_dict['notNStart']
            self.play_state = False
            self.counter.stop()
        else :
            self.counter.update()
    
    def loop(self):
        while True:
            try:
                self.recv()
                self.send()
                self.update()
            except KeyboardInterrupt:
                self.db.drop_db(self.db_name)
                quit()
        self.db.drop_db(self.tb_name)
        quit()
        
server = Server("192.168.99.50", 8000, "root", "yourname", "GAME_DB", "GAME_TB")
server.loop()