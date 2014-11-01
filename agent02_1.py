#!/usr/bin/env python

r'''
Implementation of the agent algorithm in table 23 of the IDEAL MOOC lessons.

For details see http://liris.cnrs.fr/ideal/mooc/lesson.php?n=023
'''


from itertools import cycle


# Default experiments
E1 = 'e1'
E2 = 'e2'

#Default results
R1 = 'r1'
R2 = 'r2'

#Default moods
Bored = 'BORED'
Pained = 'PAINED'
Pleased = 'PLEASED'


class Interaction(object):
    r'''Describes an agent interaction in terms of an experiment, expected result, and valence.
    '''
    def __init__(self, experiment, result, valence):
        r'''Creates a new interaction instance.

            The experiment and result are expected to be strings, while the valence should be numeric.
        '''
        self.experiment = experiment
        self.result = result
        self.valence = valence


class Agent(object):
    r'''A simple embodied agent.
    '''
    def __init__(self, *interactions):
        r'''Creates a new agent, configured to work with a given set of interactions described
            as tuples (experiment, result, valence).

            If no parameters are passed to the constructor, a default interaction set is used instead.
        '''
        if len(interactions) == 0:
            interactions = [(E1, R1, -1), (E2, R2, 1)]

        self.__experiment = interactions[0][0]
        self.interactions = dict((i[0:2], Interaction(*i)) for i in interactions)
        self.mood = Pleased

        # The cycle iterator wraps around to the beginning of the sequence after reaching its end
        self.__experiments = cycle([i[0] for i in interactions])
        self.__experiments.next() # Skips first experiment

    def experiment(self):
        r'''Returns the next experiment to try, either the same as last time (if the agent
            is currently in a pleased mood) or the next one in the list (if the agent is
            pained or bored).
        '''
        if self.mood == Pleased:
            return self.__experiment

        experiment = self.__experiments.next()
        self.__experiment = experiment
        return experiment

    def run(self, turns = 7):
        r'''Runs the agent for the specified number of turns.

            The agent will try a different experiment whenever it is pained by an interaction
            with negative valence; otherwise it keeps performing the same (pleasant) interaction.
        '''
        for i in range(0, turns):
            experiment = self.experiment()
            result = R1 if experiment == E1 else R2
            mood = self.mood

            enacted = self.interactions[experiment, result]
            mood = Pleased if enacted.valence >= 0 else Pained
            self.mood = mood

            print '%d: %s%s %s' % (i, experiment, result, mood)


def main():
    agent = Agent()
    agent.run()


if __name__ == '__main__':
    main()
