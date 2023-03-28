import sqlite3

class DB(object):
    def __init__(self, db_path):
        '''
        db_file <str> : path to database file
        '''
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
    
    def get_cursor(self):
        '''
        returns a cursor so you can interact with the habits db
        '''
        return self.conn.cursor()
    
    def commit(self):
        '''
        commit changes made to the database
        '''
        self.conn.commit()
        
    def close_connection(self):
        '''
        closes the database connection
        '''
        return self.conn.close()