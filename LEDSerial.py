import serial
from CounterTime import CounterTime
from Database import Database

class LEDSerial():
    
    def __init__(self, port, baudrate, n_w, n_h):
        self.port = port
        self.baudrate = baudrate
        self.n_w = n_w
        self.n_h = n_h
        
        self.db_save_size = 6
        self.id = 0
        self.type = 1
        self.x = 2
        self.y = 3
        self.s = 4
        self.t = 5
        
        self.ser = serial.Serial(self.port, self.baudrate)
        
        self.led_display = []
        for i in range(self.n_h):
            new = []
            for j in range(self.n_w):
                new.append('0')
            self.led_display.append(new)
        
        self.color_index = ['g', 'b']
        
        self.delay = CounterTime()
        self.delay_time = 0.07
        self.delay.restart()
        
    def save_display(self, list_db):
        self.delay.update()
        if self.delay.compare(self.delay_time):
            self.led_display = []
            for i in range(self.n_h):
                new = []
                for j in range(self.n_w):
                    new.append('0')
                self.led_display.append(new)
                
            color_i = 0
            for ls in list_db:
                if ls[self.type] == "a" :
                    x = int(ls[self.x])
                    y = int(ls[self.y])
                    self.led_display[y][x] = 'r'
                    self.ser.write('a')
                    self.ser.write(chr(x + 65))
                    self.ser.write(chr(y + 65))
                    print(x, y)
                elif ls[self.type] == "s" :
                    self.ser.write('s')
                    split_ls_x = ls[self.x].split("|")
                    split_ls_y = ls[self.y].split("|")
                    for i in range(len(split_ls_x)):
                        x = int(split_ls_x[i])
                        y = int(split_ls_y[i])
                        if x >= self.n_w :
                            x = 0
                        elif x < 0 :
                            x = self.n_w - 1
                        if y >= self.n_h :
                            y = 0
                        elif y < 0 :
                            y = self.n_h - 1
                        self.led_display[y][x] = self.color_index[color_i]
                        self.ser.write(chr(x + 65))
                        self.ser.write(chr(y + 65))
                    color_i = (color_i + 1) % len(self.color_index)
            self.delay.restart()
    
    def show(self):
        for y in self.led_display:
            for x in y:
                print x,
            print ""
        print "-------"
            
        
    def close(self):
        self.ser.close()

led_dis = LEDSerial('/dev/ttyACM0', 115200, 8, 8)

while True:
    db = Database("localhost", "root", "yourname")
    db.select_db("GAME_DB")
    ls = db.get_data("GAME_TB")
    led_dis.save_display(ls)
    # led_dis.show()
led_dis.close()
