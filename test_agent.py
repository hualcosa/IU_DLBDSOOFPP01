from agent import Agent
from habit import Habit
def test_get_all_habits():
    '''
    checks wether we can access the default habits and if there are
    five predefined habits
    '''
    a = Agent()
    print(a.habits)
    assert len(a.habits) == 5

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
    # check whether streak is being updated
    print(f'streak num before insert: {streak_before}\nstreak num after insert: {streak_after}')
    assert streak_after > streak_before

def test_get_all_habits_with_periodicity():
    '''
    check whether we are querying the database correctly and getting all habits with a prespecified periodicity
    '''
    a = Agent()
    a.get_all_habits_with_periodicity('w')
    a.get_all_habits_with_periodicity('d')
    # since I built the database, I know there must be 3 weekly and 2 daily habits among the default ones
    # Hence the first method call should return 3 lines whilst the second should return two


    

