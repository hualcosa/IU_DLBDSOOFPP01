from habit import Habit
from agent import Agent

    

# initial tests
if __name__ == '__main__':
    agent = Agent()
    print("**** Welcome to Habit Monitor! ****")
    print("This application comes with 5 prebuilt habits and one month of historical data.")
    answer = str(input("Would you like to see the predefined habits? [Y/N]\n")).lower()
    if answer == 'y':
        agent.get_all_habits()
    print('\nIf you wish to see how you can interact with the app, type: "help"')
    while True:
        input('What would you like to do next?\n')
        break
    

    # create_connection(r"C:\sqlite\db\pythonsqlite.db")
    # h1 = Habit('run', 'd')
    # h2 = Habit('workout', 'w')
    # print(h1)
    # print(h2)
