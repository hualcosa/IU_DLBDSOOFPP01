from agent import Agent
from habit import Habit


def test_get_all_habits():
    '''
    checks wether we can access the default habits and if there are
    five predefined habits
    '''
    a = Agent()
    print(a.habits)
    assert len(a.habits) >= 5 # we can have already added habits to the db

def test_create_habit():
    '''
    checks whether a habit is properly created and we stored it correctly into our database
    '''
    a = Agent()
    a.create_habit('drink water', 'd')

    print('inserting habit: Habit("drink water", "d")')
    assert ('drink water', "d") in {(h.name, h.periodicity) for h in a.habits.values()}

    c = a.database.get_cursor()
    query = f'''SELECT * FROM habits WHERE name = 'drink water' '''
    c.execute(query)
    result = c.fetchone()
    print(f"getting newly added habit from database:\n {result}")
    
    # deleting test habit from database, to keep its integrity
    query = "DELETE FROM habits WHERE name = 'drink water'"
    c.execute(query)
    a.database.commit()

def test_delete_habit():
    '''
    adds a habit then deletes it. Check whether the deletion from currently tracked habits are
    is performed correctly 
    '''
    a = Agent()
    a.create_habit('ciclying', 'd')
    a.delete_habit('ciclying')

    # was it removed from tracked habits?
    assert ('ciclying', "d") not in {(h.name, h.periodicity) for h in a.habits.values()}

    # was it removed from database?
    query = f"SELECT * FROM habits WHERE name = 'ciclying'"
    c = a.database.get_cursor()
    c.execute(query)
    assert c.fetchone() == None

def test_complete_habit():
    '''
    checks whether the habit is being completed properly.
    checks if the affected database tables are being affected properly
    '''
    a = Agent()
    c = a.database.get_cursor()
    # get the last completion date for a given habit.
    # This is being done to compare the dates pre and post insertionS
    id_ = a.habits['gym'].get_habit_id()
    len_before_insert = len(a.habits['gym'].completed_in)
    streak_before = a.habits['gym'].streak
    query = f"SELECT MAX(completion_date) FROM habits_history WHERE id = {id_}"
    c.execute(query)
    before_insert = c.fetchone()[0]

    # perform insertion
    a.complete_habit('gym')

    len_after_insert = len(a.habits['gym'].completed_in)
    streak_after = a.habits['gym'].streak
    query = f"SELECT MAX(completion_date) FROM habits_history WHERE id = {id_}"
    c.execute(query)
    after_insert = c.fetchone()[0]
    # check insertion on the database
    print(f"max date before insert: {before_insert}\n max date after insert: {after_insert}")
    assert after_insert > before_insert
    # check if the completed_in list was updapted
    print(f'len before insert: {len_before_insert}\nlen after insert: {len_after_insert}')
    assert len_after_insert > len_before_insert
    # Print streak before and after insertion
    print(f'streak num before insert: {streak_before}\nstreak num after insert: {streak_after}')

def test_get_all_habits_with_periodicity():
    '''
    check whether we are querying the database correctly and getting all habits with a prespecified periodicity
    '''
    a = Agent()
    a.get_all_habits_with_periodicity('w')
    a.get_all_habits_with_periodicity('d')
    # since I built the database, I know there must be 3 weekly and 2 daily habits among the default ones
    # Hence the first method call should return 3 lines whilst the second should return two

def test_load_predefined_habits():
    '''
    checks wether info is being correctly loaded from the database
    '''
    a = Agent()
    # if loading is working correctly, all completed_in lists should be not empty
    assert all([len(habit.completed_in) != 0 for name, habit in a.habits.items()])
    # if loading is working correctly, the streaks from predefined habits should be differen from 0
    assert all([habit.streak != 0 for name, habit in a.habits.items()])

def test_get_longest_streak():
    '''
    checks whether we are correctly getting the habit with the longest streak
    '''
    a = Agent()
    h = a.get_longest_streak()
    c = a.database.get_cursor()
    query = f'''
    SELECT h.name, t.streak
    FROM habits h
    JOIN (
        SELECT id, MAX(amount) as streak
        FROM habit_longest_streak hls
    ) t on t.id = h.id
    '''
    c.execute(query)
    habit_name, streak = c.fetchone()
    # does info from the database and loaded objects agree?
    assert h.name == habit_name and h.streak == streak
    print(f"Database info: Habit name: {habit_name} --- streak: {streak}")

def test_get_habit_longest_streak():
    '''
    since the longest streak is being stored in the habit_longest_streak table, this test
    is straightforward. It simply performs the query and evaluate the results.
    Using habit with id = 4 as example.
    '''
    a = Agent()
    c = a.database.get_cursor()
    query = f'''
    SELECT h.name, t.streak
    FROM habits h
    JOIN (
        SELECT id, amount as streak
        FROM habit_longest_streak hls
        WHERE id = 4
    ) t on t.id = h.id'''
    c.execute(query)
    habit_name, streak = c.fetchone()
    print(f"Database info: Habit name: {habit_name} --- streak: {streak}")
    assert a.habits['playing the guitar'].streak == streak

def test_query_habits_database():
    '''
    Test whether we can query the database using the "query_habits_databse" method
    '''
    a = Agent()
    query = f'''
    SELECT * 
    FROM habits h
    JOIN habits_history hh on hh.id = h.id
    JOIN habit_longest_streak hls on hls.id = h.id
    '''
    a.query_habits_database(query)


    

