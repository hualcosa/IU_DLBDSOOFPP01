import datetime
from database import DB

class Habit(object):
    def __init__(self, name, periodicity, creation_date=None):
        '''
        Constructor method. Every habit created needs to have the following parameters:
        name <str> : the name of the habit
        periodicity <str> : accepted values are 'd' for daily or 'w' for weekly
        creation_date<str>: optional. Used only to load historical data
        '''
        self.name = name
        if creation_date:
            self.creation_date = creation_date
        else:
            self.creation_date = datetime.datetime.today()
        self.periodicity = periodicity
        self.completed_in = [] # property to store the completion dates
        self.streak = 0
        self.names_dictionary = {'d': 'daily', 'w': 'weekly'}

        # defensive programming: checking whether the parameters have acceptable values
        try:
            assert self.periodicity in {'d', 'w'}
        except:
            raise Exception('incorrect value for periodicity. "d" or "w" are accepted values')
        try:
            assert len(self.name) > 0
        except:
            raise Exception('Name cannot be an empty string')
    
    def get_habit_id(self):
        '''
        Returns the habit id in the sqlite3 database
        name <str>: habit name
        '''
        db = DB('habits.db')
        query = f"SELECT id FROM habits WHERE name = '{self.name}'"
        c = db.get_cursor()
        c.execute(query)
        return c.fetchone()[0]
        
    def __str__(self) -> str:
        
        return f'Habit: {self.name}\tPeriodicty: {self.names_dictionary[self.periodicity]}\t Creation date: {self.creation_date.strftime("%Y-%m-%d")}'