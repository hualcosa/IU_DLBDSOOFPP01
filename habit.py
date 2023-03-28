import datetime


class Habit(object):
    def __init__(self, name, periodicity):
        '''
        Constructor method. Every habit created needs to have the following parameters:
        name <str> : the name of the habit
        periodicity <str> : accepted values are 'd' for daily or 'w' for weekly
        '''
        self.name = name
        self.creation_date = datetime.datetime.today()
        self.periodicity = periodicity
        self._completed_in = [] # property to store the completion dates
        self._streak = None
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
        
    def __str__(self) -> str:
        
        return f'Habit: {self.name}\tPeriodicty: {self.names_dictionary[self.periodicity]}\t Creation date: {self.creation_date.strftime("%Y-%m-%d")}'