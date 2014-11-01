#!/usr/bin/env python

r'''
Implementation of the agent algorithm in table 23 of the IDEAL MOOC lessons, with
modifications required in the programming assignment.

For details see http://liris.cnrs.fr/ideal/mooc/lesson.php?n=023
'''

from collections import namedtuple
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


class Interaction(namedtuple('_Interaction', ['experiment', 'result', 'valence'])):
    r'''Describes an agent interaction in terms of an experiment, expected result, and valence.
    '''
    pass


def Environment10(experiment):
    r'''A stateless environment where there are fixed relations between experiments
        and results.
    '''
    return R1 if experiment == E1 else R2


class Environment30(object):
    r'''An environment where an experiment's result depends on whether it was already performed
        in the previous interaction turn.
    '''
    def __init__(self):
        self.previous = E2

    def __call__(self, experiment):
        result = R1 if experiment == self.previous else R2
        self.previous = experiment
        return result


class Environment31(object):
    def __init__(self, t1 = 8, t2 = 15):
        self.clock = 0
        self.t1 = t1
        self.t2 = t2

    def __call__(self, experiment):
        self.clock += 1
        if self.clock <= self.t1 or self.clock > self.t2:
            return R1 if experiment == E1 else R2
        else:
            return R1 if experiment == E2 else R2


class Agent(object):
    r'''A simple embodied agent.
    '''
    def __init__(self, environment, *interactions):
        r'''Creates a new agent, configured to interact with th given environment through
            the given set of interactions, described as tuples (experiment, result, valence).

            If no interactions are passed to the constructor, a default interaction set is used instead.
        '''
        if len(interactions) == 0:
            interactions = [(E1, R1, -1), (E1, R2, 1), (E2, R1, -1), (E2, R2, 1)]

        self.__experiments = [i[0] for i in interactions]
        self.environment = (lambda s, e: environment(e)).__get__(self, Agent)
        self.primitives = dict((i[0:2], Interaction(*i)) for i in interactions)
        self.composites = dict()
        self.context = None
        self.mood = Pleased

    def anticipate(self):
        r'''Returns a list of next likely interactions (according to this agent's own previous
            experience) given the last enacted interaction, or None if such a list does not
            yet exist.
        '''
        return self.composites.get(self.context, None)

    def another(self, experiments, fallback = None):
        r'''Returns an experiment not in the given collection, or the fall back experiment
        if one couldn't be found among this agent's known experiments.
        '''
        for e in self.__experiments:
            if not e in experiments:
                return e

        return fallback

    def select(self, anticipations):
        r'''Given a list of anticipated interactions, look for an interaction of positive
            valence and return its associated experiment. If none could be found, return
            an experiment not associated to any of the anticipated interactions.
        '''
        for anticipated in anticipations:
            print 'afforded %s%s,%d' % (anticipated.experiment, anticipated.result, anticipated.valence)

        anticipated = anticipations[0]
        if anticipated.valence > 0:
            return anticipated.experiment

        return self.another({a.experiment for a in anticipations}, anticipated.experiment)

    def experiment(self):
        r'''Select the next experiment to perform.
        '''
        anticipations = self.anticipate()
        if anticipations != None:
            return self.select(anticipations)
        elif self.context == None:
            return self.__experiments[0]
        elif self.mood == Pleased:
            return self.context.experiment
        else:
            return self.another({self.context.experiment})

    def learn(self, enacted):
        r'''Records a new composite interaction composed of the just-enacted primitive
            interaction and its predecessor.
        '''
        context = self.context
        self.context = enacted
        if context == None:
            return

        anticipated = self.composites.setdefault(context, [])
        if not enacted in anticipated:
            anticipated.append(enacted)
            anticipated.sort(lambda x, y: y.valence - x.valence)
            print 'learn %s%s%s%s' % (context.experiment, context.result, enacted.experiment, enacted.result)

    def run(self, turns = 10):
        r'''Runs the agent for the specified number of turns.

            The agent starts by trying the first experiment on its list, moving to alternatives
            only if it gets negative results. Over time however, it builds a list of composite
            interactions that enable it to decide what experiment to try next based on last
            turn's enacted interaction.
        '''
        for i in range(0, turns):
            experiment = self.experiment()
            result = self.environment(experiment)
            mood = self.mood

            enacted = self.primitives[experiment, result]
            print 'Enacted %s%s,%d' % enacted

            self.learn(enacted)

            mood = Pleased if enacted.valence >= 0 else Pained
            self.mood = mood
            print '%d: %s' % (i, mood)


def main():
    #agent = Agent(Environment10)
    #agent = Agent(Environment30())
    agent = Agent(Environment31())
    agent.run(20)


if __name__ == '__main__':
    main()
