import MySQLdb

class Database():
    
    def __init__(self, addr, user, pwd):
        self.addr = addr
        self.user = user
        self.pwd = pwd
        
        self.db = MySQLdb.connect(self.addr, self.user, self.pwd)
        self.cursor = self.db.cursor()
        self.data = []
    
    def get_db(self):
        self.cursor.execute("SHOW DATABASES;")
        ls = self.cursor.fetchall()
        arr = []
        for l in ls:
            arr.append(l[0])
        return arr
    
    def create_db(self, db_name):
        if db_name in self.get_db():
            self.select_db(db_name)
        else :
            self.cursor.execute("CREATE DATABASE `" + db_name  + "`;")
            self.select_db(db_name)
            
    def select_db(self, db_name):
        if db_name in self.get_db():
            self.cursor.execute("USE `" + db_name + "`;")
        else :
            self.create_db(db_name)
    
    def drop_db(self, db_name):
        if db_name in self.get_db():
            self.cursor.execute("DROP DATABASE `" + db_name + "`;")
    
    def list_tb(self):
        self.cursor.execute("SHOW TABLES;")
        list_tb = self.cursor.fetchall()
        arr = []
        for l in list_tb:
            arr.append(l[0])
        return arr
    
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
    
    def drop_tb(self, tb_name):
        if tb_name in self.list_tb():
            self.cursor.execute("DROP TABLE `" + tb_name + "`;")

    def get_list_data(self, tb_name):
        self.cursor.execute("SELECT * FROM `" + tb_name +"`;")
        self.data = list(self.cursor.fetchall())
        return self.data

    def index_data(self, tb_name, index, find):
        for i in range(len(self.get_list_data(tb_name))):
            if self.data[i][index] == find:
                return index
        return -1

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
        else :
            self.update_data(tb_name, _id, typ, x, y, s, t)
    
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
        else :
            self.insert_data(tb_name, _id, typ, x, y, s, t)
    
    def delete_data(self, tb_name, _id):
        if self.index_data(tb_name, 0, _id) >= 0:
           self.cursor.execute("DELETE FROM `"+ tb_name +"` WHERE `id`='" + _id + "'")
           
    def get_data(self, tb_name):
        return self.get_list_data(tb_name)
    
    def close(self):
        self.db.close()