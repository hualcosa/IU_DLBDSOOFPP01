from database import DB
from habit import Habit
from datetime import datetime, timedelta
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
        # dictionary to store the currently tracked habits
        self.habits = {'gym': Habit('gym', 'd'),
                       'hiking': Habit('hiking', 'w'),
                       'swimming': Habit('swimming', 'w'),
                       'playing the guitar': Habit('playing the guitar', 'd'),
                       'learn german': Habit('learn german', 'w')}
        
        # load habit history and streak from the database
        load_predefined_data()    
    
    def load_predefined_data(self):
        TODO

    def create_habit(self, name, periodicity):
        '''
        name <str>: Habit name
        Periodicity <str>: Habit periodicity. Acepted values: 'w', 'd' 

        Creates a habit, add it to the list of currently tracked habits and persist it on the database
        '''
        h = Habit(name, periodicity)
        self.habits[name] = h
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
        del self.habits[name]
                
                
        # delete habit from the database
        query = f'DELETE FROM habits WHERE name = "{name}"'
        c = self.database.get_cursor()
        c.execute(query)
        self.database.commit()
        
    def complete_habit(self, name):
        '''
        name <str>: Habit name
        Completes a task. Checks wether we are on a streak or we broke the habit
        '''
        completion_date = datetime.now()
        self.habits[name].completed_in.append(completion_date)
        self.check_streak(self.habits[name], completion_date)

        # getting habit id from db
        id_ = self.habits[name].get_habit_id() 
        # add completion_info to db
        query = f"INSERT INTO habits_history (id, completion_date) VALUES ({id_}, '{completion_date}')"
        c = self.database.get_cursor()
        c.execute(query)
        self.database.commit()
        # add streak info to db
        query = f"INSERT INTO habit_streak (id, periodicity, amount) VALUES ({id_}, '{self.habits[name].periodicity}', '{self.habits[name].streak}')"
        c = self.database.get_cursor()
        c.execute(query)
        self.database.commit()
        
    
    def check_streak(self, habit, completion_date):
        # control flow to deal with streak condition according to periodicity
        is_empty = len(habit.completed_in) == 1 # if true, means we are completing for the first time
        if is_empty:
            habit.streak = 1
        else:
            last_completed_date = habit.completed_in[-1]
            if habit.periodicity == 'w':
                streak_condition = completion_date.isocalendar().week == last_completed_date.isocalendar().week + 1
            else:
                streak_condition = completion_date.day == (last_completed_date.day + 1)
            
            if streak_condition: 
                habit.streak += 1
                # check wether it is necessary to update habit_longest_streak table
                TODO
            else:
                print("Oh sorry, you broke the habit :(")
                habit.streak = 1 # broke the habit


    def get_all_habits(self):
        '''
        return all currently tracked habits by the application
        '''
        # query the database and get fetch answers
        c = self.database.get_cursor()
        c.execute("SELECT name FROM habits")

        habits_list = ([h[0] for h in c.fetchall()])
        print(f'All habits we monitor so far are: {habits_list}')

    def get_all_habits_with_periodicity(self, periodicity):
        '''
        return all habits with the same periodicity
        periodicity <str>: accepted values: 'd', 'w'
        '''
        query = f"SELECT * FROM habits WHERE periodicity = '{periodicity}'"
        c = self.database.get_cursor()
        c.execute(query)
        print('[', 'id', 'name', 'creation_date', 'periodicity', ']')
        for h in c.fetchall():
            print(h)

    def get_longest_streak(self):
        pass
    def get_habit_longest_streak(self):
        pass
    def query_habits_database(self, query):
        pass


