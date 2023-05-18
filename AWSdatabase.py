import sqlite3
import os.path
from os import path

class UserDB():

    def __init__(self):
        self.conn = None
        self.c = None

        if UserDB.db_exist(self):
            UserDB.connect_db(self)
        else:
            UserDB.create_user_db(self)

        print("DB Initialized")

    def db_exist(self):
        return path.exists('database/aws.db')

    def create_user_db(self):
        UserDB.connect_db(self)
        if not UserDB.table_exist(self):
            UserDB.create_table(self)
        
    def connect_db(self):
        self.conn = sqlite3.connect('database/aws.db',check_same_thread=False)
        # self.c = self.conn.cursor()
        print("DB Connected")

    def table_exist(self):
        self.c = self.conn.cursor()
        self.c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='awslist' ''')
        if self.c.fetchone()[0]==1 : 
            # self.conn.close()
            return True
        else: 
            # self.conn.close()
            return False

    def create_table(self):
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE awslist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            awsid TEXT,
            Plastic TEXT,
            Paper TEXT,
            Metal TEXT,
            Waste TEXT,
            Battery TEXT
        )""")
        self.conn.commit()
        self.conn.close()
        print("database created")

    def UpdateData(self,q):
        sql = "UPDATE awslist SET Plastic = '"+q[0]+"', Waste = '"+q[1]+"', Paper = '"+q[2]+"', Metal = '"+q[3]+"', Battery = '"+q[4]+"' WHERE awsid = '"+q[5]+"'"
        self.c = self.conn.cursor()
        data = self.c.execute(sql)
        self.conn.commit()
        print("Record Updated successfully")
        print(sql)
        self.c.close()
        return [q]
    
    def UpdateSingleData(self,q,col):
        sql = "UPDATE awslist SET "+col.capitalize()+" = '"+q[0]+"', Battery = '"+q[1]+"' WHERE awsid = '"+q[2]+"'"
        self.c = self.conn.cursor()
        data = self.c.execute(sql)
        self.conn.commit()
        print("Record Updated successfully")
        print(sql)
        self.c.close()
        return [q]

    def getStatus(self,id):
        self.c = self.conn.cursor()
        data = self.c.execute("SELECT * from awslist WHERE awsid = '"+id+"'").fetchall()
        self.conn.close()
        print(data)
        return data

    def getStatusall(self):
        self.c = self.conn.cursor()
        data = self.c.execute('SELECT * from awslist').fetchall()
        self.conn.close()
        return data
    
    def awsIDExist(self,id):
        self.c = self.conn.cursor()
        row = self.c.execute("SELECT * from awslist WHERE awsid='"+id+"'").fetchall()
        if row is None:
            # self.conn.close()
            return False
        # self.conn.close()
        return True
    
    
    def addNewAWS(self,id):
        if UserDB.awsIDExist(self,id):
            self.c = self.conn.cursor()
            data = self.c.execute('INSERT INTO awslist (awsid,Plastic,Paper,Metal,Waste,Battery) VALUES (?,?,?,?,?,?)',[str(id),"0","0","0","0","0"])
            self.conn.commit()
            self.c.close()
            return data
        return "Exist"

    def conn_close(self):
        self.conn.close()
