import MySQLdb

class Database():
    
    def __init__(self, addr, user, pwd):    # Set data 
        self.addr = addr    # IP
        self.user = user    # Username of mysql
        self.pwd = pwd      # Password of mysql
        
        self.db = MySQLdb.connect(self.addr, self.user, self.pwd)   # Connect to mysql
        self.cursor = self.db.cursor()  # set cursor
        self.data = []  # Data from database
    
    # List of database name
    def get_db(self):
        self.cursor.execute("SHOW DATABASES;")
        ls = self.cursor.fetchall()
        arr = []
        for l in ls:
            arr.append(l[0])
        return arr
    
    # Create database
    def create_db(self, db_name):
        if db_name in self.get_db():    # Database is created => Select database
            self.select_db(db_name)
        else :
            self.cursor.execute("CREATE DATABASE `" + db_name  + "`;")
            self.select_db(db_name)
            
    # Select Database
    def select_db(self, db_name):   
        if db_name in self.get_db():
            self.cursor.execute("USE `" + db_name + "`;")
        else :  # Database is not created => Create database
            self.create_db(db_name)
    
    # Drop database
    def drop_db(self, db_name):
        if db_name in self.get_db():    # See this database => drop database
            self.cursor.execute("DROP DATABASE `" + db_name + "`;")
    
    # List of table
    def list_tb(self):
        self.cursor.execute("SHOW TABLES;")
        list_tb = self.cursor.fetchall()
        arr = []
        for l in list_tb:
            arr.append(l[0])
        return arr
        
    # Crete table
    def create_tb(self, tb_name):
        if not(tb_name in self.list_tb()):
            self.cursor.execute("CREATE TABLE `" + tb_name + \
                                "` (`id` VARCHAR(10),\
                                `type` VARCHAR(3),\
                                `x` TINYTEXT,\
                                `y` TINYTEXT,\
                                `s` SMALLINT,\
                                `t` SMALLINT,\
                                PRIMARY KEY(`id`));")
    
    # Drop table
    def drop_tb(self, tb_name):
        if tb_name in self.list_tb():
            self.cursor.execute("DROP TABLE `" + tb_name + "`;")

    # Get data in this table
    def get_list_data(self, tb_name):
        self.cursor.execute("SELECT * FROM `" + tb_name +"`;")
        self.data = list(self.cursor.fetchall())
        return self.data

    # Get index of data
    def index_data(self, tb_name, index, find):
        for i in range(len(self.get_list_data(tb_name))):
            if self.data[i][index] == find:
                return index
        return -1

    # Insert data
    def insert_data(self, tb_name, _id, typ, x, y, s, t):
        if self.index_data(tb_name, 0, _id) < 0:
            self.cursor.execute("INSERT INTO `" + tb_name + \
                                "` (`id`,`type`,`x`,`y`,`s`,`t`) \
                                VALUES ('" +
                            str(_id) + "', '" +
                            str(typ) + "','" +
                            str(x) + "','"+
                            str(y) + "','" +
                            str(s) + "','" +
                            str(t) + "');")
            self.db.commit()
        else :  # If data is creted => update it
            self.update_data(tb_name, _id, typ, x, y, s, t)
    
    # Update data
    def update_data(self, tb_name, _id, typ, x, y, s, t):
        if self.index_data(tb_name, 0, _id) >= 0:
            self.cursor.execute("UPDATE `" + tb_name + "` " +
                            "SET `type`='" + str(typ) +
                            "', `x`='" + str(x) +
                            "', `y`='" + str(y) +
                            "', `s`='" + str(s) +
                            "', `t`='" + str(t) +
                            "' WHERE `id`='" + str(_id) +"';")
            self.db.commit()
        else :      # Data is not created => Insert it
            self.insert_data(tb_name, _id, typ, x, y, s, t)
    
    # Delete data
    def delete_data(self, tb_name, _id):
        if self.index_data(tb_name, 0, _id) >= 0:
           self.cursor.execute("DELETE FROM `"+ tb_name +"` WHERE `id`='" + _id + "'")
           
    # Get data from table
    def get_data(self, tb_name):
        return self.get_list_data(tb_name)
    
    # Disconnect database
    def close(self):
        self.db.close()