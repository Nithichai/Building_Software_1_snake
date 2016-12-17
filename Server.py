import socket
import time
import random
from TileManager import TileManager
from Database import Database
from Apple import Apple
from CounterTime import CounterTime

APPLE = "a"

class Server():
    
    def __init__(self, host, port, user, pwd, db_name, tb_name):
        self.host = host        # IP Server
        self.port = port        # Port
        self.user = user        # mysql username
        self.pwd = pwd          # password mysql
        self.db_name = db_name  # database name
        self.tb_name = tb_name  # table name
    
        self.max_player = 3     # maximum player
        # State  of server
        # OK = run game
        # notNStart = player not enough to play at before start game
        # notNExit = player not enough to play at after start game
        self.server_state_dict = {'OK':0, 'notNStart':1, 'notNExit':2}  
        self.server_state = self.server_state_dict['notNStart']         # State of server
        self.play_state = False                                         # State of start to play game
        self.addr = None
        
        self.db_save_size = 6   # Column size of data base
        self.id = 0             # index of database's column
        self.type = 1
        self.x = 2
        self.y = 3
        self.s = 4
        self.t = 5
        
        self.counter = CounterTime()    # Game Timer
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Start socket
        self.sock.bind((self.host, self.port))                          # Connect to host and port
        self.sock.settimeout(1)
        print("Server start...")
        
        self.db = Database("localhost", self.user, self.pwd)            # Connect mysql
        self.db.create_db(self.db_name)                                 # Create database
        self.db.create_tb(self.tb_name)                                 # Create table in database
        print("Database start....")
        
    # Received data from client   
    def recv(self):
        try :
            packet, self.addr = self.sock.recvfrom(1024)    # Get data from client
            if packet == None: # If see none
                return  # exit this method
            if packet.find("tile:") != -1:                  # If see "tile:" 
                first_index = packet.find(":") + 1          # Get index
                new_packet = packet[first_index:]           # Substring
                ls = new_packet.split(",")                  # Split new_packet
                self.tile_mng = TileManager(int(ls[0]), int(ls[1]), int(ls[2]), int(ls[3])) # Set tileManager
                self.apple_x = random.randrange(0, self.tile_mng.get_nw_tile())     # Random x of apple
                self.apple_y = random.randrange(0, self.tile_mng.get_nh_tile())     # Random y of apple
                self.db.insert_data(self.tb_name, "*", APPLE, self.apple_x, self.apple_y, 0, 0)   # Insert Apple data to database
            elif packet == "eaten" :        # If see "eaten"
                self.apple_x = random.randrange(0, self.tile_mng.get_nw_tile()) # Random x of apple
                self.apple_y = random.randrange(0, self.tile_mng.get_nh_tile()) # Random y of apple
                self.db.insert_data(self.tb_name, "*", APPLE, self.apple_x, self.apple_y, 0, 0)   # Insert Apple data to database
            elif packet == "stop" :     # If see "stop"
                self.counter.stop()     # Stop timer
            else :  # Otherwise => Get Snake data from client
                ls_client = packet.split(",")   # Split data
                self.db.insert_data(self.tb_name,   # Insert snake data to database
                                    ls_client[self.id],
                                    ls_client[self.type],
                                    ls_client[self.x],
                                    ls_client[self.y],
                                    ls_client[self.s],
                                    int(self.counter.get_time()))   # Game's time
        except socket.timeout :
            print("Error : Server recv timeout")
    
    # Send data to client
    def send(self):
        packet = ""     # Make string packet
        if self.server_state == self.server_state_dict['notNStart']:    # State server is notNStart
            packet = "notNStart"    # Set packet "notNStart"
        elif self.server_state == self.server_state_dict['notNExit']:   # State server is notNExit
            packet = "notNExit"     # Set packet "notNExit"
        else :  # Otherwise
            ls_data = self.db.get_data(self.tb_name)    # Get data from database
            packet = "*,a," + str(self.apple_x) + "," + str(self.apple_y) + ",0,0/" # Set apple set packet
            for ls in ls_data:      # Set data from row of database
                for i in range(self.db_save_size-1):    # Indexing from row of database
                    packet += str(ls[i]) + "," # Set snake's data to packet
                packet += str(int(self.counter.get_time())) # Pack time of game in database
                packet += "/"   # Pack one snake
            packet = packet[:-1]    # Not select final "/"
        if self.addr != None :
            self.sock.sendto(packet, self.addr) # Send to client
    
    # Update Server
    def update(self):
        if len(self.db.get_data(self.tb_name)) >= self.max_player and not self.play_state : # Player enough and not playing
            self.server_state = self.server_state_dict['OK']    # State = OK
            self.play_state = True  # Play state is true
            self.counter.restart()  # Start game time
        elif len(self.db.get_data(self.tb_name)) < self.max_player and self.play_state : # Player not enough and playing
            self.server_state = self.server_state_dict['notNExit']  # State = notNExit
            self.play_state = False # Stop playing
            self.counter.stop()     # Stop game time
        elif len(self.db.get_data(self.tb_name)) < self.max_player and not self.play_state :    # Player not enough and not playing 
            self.server_state = self.server_state_dict['notNStart'] # State = notNStart
            self.play_state = False     # Stop playing
            self.counter.stop()         # Stop game time
        else :  # Otherwise
            self.counter.update()       # Update game time
    
    # Server loop to pacl recv, send, update
    def loop(self):
        while True:
            try:
                self.recv() # Received data from client
                self.send() # Send data to client
                self.update()   # Update server
            except KeyboardInterrupt:   # If stop program by keyboard
                self.db.drop_db(self.db_name)   #Drop database
                quit()  # Quit program
        self.db.drop_db(self.tb_name)   #Drop database
        quit() # Quit program
        
server = Server(raw_input("IP : "), 8000, "root", "yourname", "GAME_DB", "GAME_TB") # Start to use Server
server.loop()   # Use server's loop