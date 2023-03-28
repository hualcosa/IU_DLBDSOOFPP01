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
    assert ('drink water', "d") in {(h.name, h.periodicity) for h in a.habits}

    c = a.database.get_cursor()
    query = f'''SELECT * FROM habits WHERE name = 'drink water' '''
    c.execute(query)
    result = c.fetchone()
    print(f"getting newly added habit from database:\n {result}")

def test_delete_habit():
    '''
    adds a habit then deletes it. Check whether the deletion from currently tracked habits are
    is performed correctly 
    '''
    a = Agent()
    a.create_habit('ciclying', 'd')
    a.delete_habit('ciclying')

    # was it removed from tracked habits?
    assert ('ciclying', "d") not in {(h.name, h.periodicity) for h in a.habits}

    # was it removed from database?
    query = f"SELECT * FROM habits WHERE name = 'ciclying'"
    c = a.database.get_cursor()
    c.execute(query)
    assert c.fetchone() == None

