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
        self.habits = {}
        
        # load habit history and streak from the database
        self.load_predefined_data()    
    
    def load_predefined_data(self):
        '''
        Load the habits, history and streak info to the habit objects created in self.habits
        '''
        # loading habits from db
        c = self.database.get_cursor()
        query = f"SELECT name, creation_date, periodicity FROM habits"
        c.execute(query)
        for name, creation_date, periodicity in c.fetchall():
            self.habits[name] = Habit(name, periodicity, creation_date)

        # loading habits history
        for name, habit in self.habits.items():
            query = f'''
            SELECT completion_date
            FROM habits_history hh
            JOIN habits h ON hh.id = h.id
            WHERE h.name = '{name}'
            '''
            c.execute(query)
            # load data to the list of dates where the habit was completed
            for tup in c.fetchall():
                habit.completed_in.append(tup[0])

            # load th streak info
            query = f'''
            SELECT amount 
            FROM habit_longest_streak hls
            JOIN habits h ON h.id = hls.id
            WHERE h.name = '{name}'
            '''
            try:
                c.execute(query)
                habit.streak = c.fetchone()[0]
            except:
                continue # in case the habit hasn't been completed yet, no streak info will be available in the tables
        


    def create_habit(self, name, periodicity):
        '''
        name <str>: Habit name
        Periodicity <str>: Habit periodicity. Acepted values: 'w', 'd' 

        Creates a habit, add it to the list of currently tracked habits and persist it on the database
        '''
        h = Habit(name, periodicity)
        self.habits[name] = h
        habit_id = len(self.habits)
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
        print(f"Habit: {name} succesfully deleted !!!")
        
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
        print("Habit completed!!!")
    
    def check_streak(self, habit, completion_date):
        '''
        habit <Habit>: Habit Object 
        completion date <datetime>: habit completion date
        '''
        # control flow to deal with streak condition according to periodicity
        is_empty = len(habit.completed_in) == 1 # if true, means we are completing for the first time
        if is_empty:
            habit.streak = 1
            # insert record in the habit longest streak table
            id_ = habit.get_habit_id()
            query = f"INSERT INTO habit_longest_streak (id, amount) VALUES ({id_}, 1)"
            c = self.database.get_cursor()
            c.execute(query)
            self.database.commit()
        else:
            last_completed_date = habit.completed_in[-1]
            if habit.periodicity == 'w':
                streak_condition = completion_date.isocalendar().week == last_completed_date.isocalendar().week + 1
            else:
                streak_condition = completion_date.day == (last_completed_date.day + 1)
            
            if streak_condition: 
                habit.streak += 1
                # check wether it is necessary to update habit_longest_streak table
                c = self.database.get_cursor()
                query = f'''
                SELECT amount
                FROM habit_longest_streak hls
                JOIN habit h ON h.id = hls.id
                WHERE name = '{habit.name}' 
                '''
                c.execute()
                amount = c.fetchone()[0]
                if amount > habit.streak:
                    # update the object
                    habit.streak = amount
                    # add streak info to db
                    id_ = habit.get_habit_id()
                    query = f"UPDATE habit_longest_streak SET amount = {amount} WHERE id = {id_})"
                    c = self.database.get_cursor()
                    c.execute(query)
                    self.database.commit()
            else:
                # if we complete the habit on the same period, I decided not to increase the streak.E.g complete a daily habit twice in a day won't increase the habit
                if completion_date.day != last_completed_date.day:
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
        return habits_list

    def get_all_habits_with_periodicity(self, periodicity):
        '''
        return all habits with the same periodicity
        periodicity <str>: accepted values: 'd', 'w'
        '''
        query = f"SELECT * FROM habits WHERE periodicity = '{periodicity}'"
        c = self.database.get_cursor()
        c.execute(query)
        
        return c.fetchall()

    def get_longest_streak(self):
        '''
        returns the habit with the longest streak among all habits being tracked
        '''
        longest_streak = 0
        ls_habit = None
        for h in self.habits.values():
            if h.streak > longest_streak:
                longest_streak = h.streak
                ls_habit = h

        return ls_habit

    def get_habit_longest_streak(self, name):
        '''
        returns the logest streak for a habit
        name <str>: habit name
        '''
        try:
            return self.habits[name].streak
        except:
            print("Invalid habit name. Try again with a valid habit name")
    
    def query_habits_database(self, custom_query):
        '''
        perfom a custom SQL query in the habits db .
        custom query <str>: sql query
        '''
        print(custom_query)
        c = self.database.get_cursor()
        try:
            c.execute(custom_query)
            print(f"\nanswer:\n{c.fetchall()}")

        except Exception as e:
            print("There is an error in your SQL query:\n\n")



