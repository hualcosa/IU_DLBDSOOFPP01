from habit import Habit
from agent import Agent
import re

    

# Entry point
if __name__ == '__main__':
    agent = Agent()
    print("**** Welcome to Habit Monitor! ****")
    print("This application comes with 5 prebuilt habits and one month of historical data.")
    answer = str(input("Would you like to see the predefined habits? [Y/N]\n")).lower()
    if answer == 'y':
        habits_list = agent.get_all_habits()
        print(f'All habits we monitor so far are: {habits_list}')
    print('\nIf you wish to see how you can interact with the app, type: "help"')
    while True:
        answer = input('What would you like to do next?\n').lower()
        if answer == "help":
            print('''
            ATTENTION! To sucessffully execute the commands you sould NOT use quotation marks
            when writing the habit name

            create_habit <habit_name> <habit_periodicity>
            delete_habit <habit_name> 
            complete_habit <habit_name>
            quit

            analyze <operation_number> <additional_parameters>
            operation_number:
                1: list all current habits tracked
                2: list all habits with the same periodicity. Additional parameter – Periodicity: d, w,
m (daily, weekly or monthly).
                3: get longest run streak among all habits being tracked
                4: get longest run streak for a give habit. Additional parameter - habit_name
                5: Ask custom question. This operation allows the user to query the application’s
database using SQL. Additional parameter: <sql_query>
            ''')
        
        if answer == 'quit':
            break
        if re.match(r"create_habit\s([\w\s]+)\s([dw])", answer):
            match = re.match(r"create_habit\s([\w\s]+)\s([dw])", answer)
            habit_name, periodicity = match.group(1), match.group(2)
            # defensive programming. Avoiding user inserting habit already monitored
            if habit_name in {n for n in agent.habits.keys()}:
                print("habit already being tracked")
            else:
                agent.create_habit(habit_name, periodicity)
                print("Habit successfully created!!!")

        if re.match(r"delete_habit\s([\w\s]+)", answer):
            match = re.match(r"delete_habit\s([\w\s]+)", answer)
            habit_name = match.group(1)

            # defensive programming: Only delete a habit in case it exists
            if habit_name in {n for n in agent.habits.keys()}:
                agent.delete_habit(habit_name)
            

        if re.match(r"complete_habit\s([\w\s]+)", answer):
            match = re.match(r"complete_habit\s([\w\s]+)", answer)
            habit_name = match.group(1)
            agent.complete_habit(habit_name)

        if re.match(r"analyze\s(\d)([\s\w]+)?", answer):
            match  = re.match(r"analyze\s(\d)(.+)?", answer)
            op_number = int(match.group(1))
            if op_number == 1:
                habits_list = agent.get_all_habits()
                print(f'All habits we monitor so far are: {habits_list}')

            elif op_number == 2:
                periodicity = match.group(2).strip() # remove excess spaces
                habits = agent.get_all_habits_with_periodicity(periodicity)
                print('[', 'id', 'name', 'creation_date', 'periodicity', ']')
                for h in habits:
                    print(h)

            elif op_number == 3:
                ls_habit = agent.get_longest_streak()  
                print(f"The habit with the longest streak is:\nHabit name: {ls_habit.name} --- periodicity: {ls_habit.periodicity} --- streak: {ls_habit.streak} periods")
            elif op_number == 4:
                habit_name = match.group(2).strip() # remove excess spaces
                streak = agent.get_habit_longest_streak(habit_name)
                print(f"Habit Name: {habit_name} --- Longest Streak: {streak}")

            elif op_number == 5:
                sql_query = match.group(2).strip() # remove excess spaces
                agent.query_habits_database(sql_query)
            else:
                print("Invalid operation number. Type 'help' to check the docs if necessary.")
        
