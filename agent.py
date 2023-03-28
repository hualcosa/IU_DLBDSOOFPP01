from database import DB
from habit import Habit
from datetime import datetime
class Agent(object):
    '''
    This class represents a virtual assitant that perform the operation
    on the application
    '''
    def __init__(self) -> None:
        '''
        Constructor method. Creates a database to the database and
        set the default habits 
        '''
        self.database = DB('habits.db')
        self.habits = [Habit('gym', 'd'),
                       Habit('hiking', 'w'),
                       Habit('swimming', 'w'),
                       Habit('playing the guitar', 'd'),
                       Habit('learn german', 'w')]    
    
    def create_habit(self, name, periodicity):
        '''
        name <str>: Habit name
        Periodicity <str>: Habit periodicity. Acepted values: 'w', 'd' 

        Creates a habit, add it to the list of currently tracked habits and persist it on the database
        '''
        h = Habit(name, periodicity)
        self.habits.append(h)
        habit_id = len(self.habits) + 1
        habit_creation_date = datetime.now().strftime('%Y-%m-%d')
        query = f"INSERT INTO habits (id, name, creation_date, periodicity) VALUES ({habit_id}, '{name}', '{habit_creation_date}', '{periodicity}')"
        
        c = self.database.get_cursor()
        c.execute(query)
        self.database.commit()

    def delete_habit(self, name):
        '''
        name <str>: name of the habit to be deleted.

        Deletes a habit from the tracked habits and from the database. 
        '''
        # delete habit from the habits list
        for i,h in enumerate(self.habits):
            if h.name == name:
                del self.habits[i]
                
        # delete habit from the database
        query = f'DELETE FROM habits WHERE name = "{name}"'
        c = self.database.get_cursor()
        c.execute(query)
        self.database.commit()
        
    def complete_habit(self, name):
        pass
    def get_all_habits(self):
        '''
        return all currently tracked habits by the application
        '''
        # query the database and get fetch answers
        c = self.database.get_cursor()
        c.execute("SELECT name FROM habits")

        habits_list = ([h[0] for h in c.fetchall()])
        print(f'All habits we monitor so far are: {habits_list}')

    def get_all_habits_with_periodicity(self, name, periodicity):
        pass
    def get_longest_streak(self):
        pass
    def get_habit_longest_streak(self):
        pass
    def query_habits_database(self, query):
        pass


