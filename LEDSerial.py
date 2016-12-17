import serial
from CounterTime import CounterTime
from Database import Database

class LEDSerial():
    
    def __init__(self, port, baudrate, n_w, n_h):
        self.port = port            # Set port of arduino
        self.baudrate = baudrate    # Set baudrate of arduino
        self.n_w = n_w              # number of tile's game in x
        self.n_h = n_h              # number of tile's game in y
        
        self.db_save_size = 6       # Size of column of database
        self.id = 0
        self.type = 1
        self.x = 2
        self.y = 3
        self.s = 4
        self.t = 5
        
        self.ser = serial.Serial(self.port, self.baudrate)  # Set serial
        
        self.led_display = []   # Array of data
        
        # Set 1d to  2d array and set all data to '0' in table
        self.restart_table()
        
        self.color_index = ['g', 'b']   # Color's code of snake
        
        self.delay = CounterTime()  # Set timer for send data to serial
        self.delay_time = 0.07      # Delay of send data to serial
        self.delay.restart()        # Start send's timer
    
    def restart_table(self):
        self.led_display = [] 
        for i in range(self.n_h):
            new = []
            for j in range(self.n_w):
                new.append('0')
            self.led_display.append(new)
        
    # Set all data into table (list_db use with datas from database)
    def save_display(self, list_db):
        self.delay.update()     # Update send timer
        if self.delay.compare(self.delay_time):     # Time of sending timer more than delay time
            self.restart_table() # Restart table
            color_i = 0     # Set color index (index of color_index)
            for ls in list_db:      # Loop in list_db
                if ls[self.type] == "a" :   # if see apple in data (type = a is apple)
                    x = int(ls[self.x])     # set string of x,y to integer
                    y = int(ls[self.y])
                    self.led_display[y][x] = 'r'    # set table that index is (x,y) is 'r' (red)
                    self.ser.write('a')     # send 'a' to serial
                    self.ser.write(chr(x + 65)) # send data of x to serial
                    self.ser.write(chr(y + 65)) # send data of y to serial
                    print(x, y)
                elif ls[self.type] == "s" :     # see type is smake
                    self.ser.write('s')         # send 's' to serial
                    split_ls_x = ls[self.x].split("|")  # split all x postion 
                    split_ls_y = ls[self.y].split("|")  # split all y postion
                    for i in range(len(split_ls_x)):
                        x = int(split_ls_x[i])  # set string of x,y to integer
                        y = int(split_ls_y[i])
                        if x >= self.n_w :      # if postion is right more than of frame
                            x = 0               # set to left of frama
                        elif x < 0 :            # if postion is  left more than of frame
                            x = self.n_w - 1    # set to right of frame
                        if y >= self.n_h :      # if postion is below than frame
                            y = 0               # set to above of frame
                        elif y < 0 :            # if postion is above than frame
                            y = self.n_h - 1    # set to below of frame
                        self.led_display[y][x] = self.color_index[color_i]  # set data in table
                        self.ser.write(chr(x + 65)) # send x, y to serial
                        self.ser.write(chr(y + 65))
                    color_i = (color_i + 1) % len(self.color_index)     # change color's index
            self.delay.restart()
    
    # Show table in terminal
    def show(self):
        for y in self.led_display:  # Loop for y
            for x in y:     # Loop for x
                print x,
            print ""
        print "-------"
            
    # Close serial port
    def close(self):
        self.ser.close()

led_dis = LEDSerial('/dev/ttyACM0', 115200, 8, 8)   # Set port, buadrate and number of tile

while True: # Loop forever
    try :
        db = Database("localhost", "root", "yourname")      # Set database
        db.select_db("GAME_DB")                             # Select database
        ls = db.get_data("GAME_TB")                         # Get data from database
        led_dis.save_display(ls)                            # Save data into table
        # led_dis.show()
    except KeyboardInterrupt:
        led_dis.close()     # Close serial
led_dis.close()     # Close serial
