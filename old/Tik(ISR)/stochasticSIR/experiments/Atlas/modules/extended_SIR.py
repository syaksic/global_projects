from nepidemix.process import ExplicitStateProcess

from nepidemix.utilities.networkxtra import attributeCount, neighbors_data_iter

import numpy


class SIRProcess(ExplicitStateProcess):
    """
    S I R process,

    Attributes
    ----------
    beta - Infection rate.
    gamma - Recovery rate.
    """
    def __init__(self, _lambda, _delta, _xi, _alpha, _beta, _eta):

        super(SIRProcess, self).__init__(['I', 'S', 'R'],
                                         [],
                                         runNodeUpdate = True,
                                         runEdgeUpdate = False,
                                         runNetworkUpdate = False,
                                         constantTopology = True)
        self._lambda=float(_lambda)
        self._delta=float(_delta)
        self._xi=float(_xi)
        self._alpha=float(_alpha)
        self._beta=float(_beta)
        self._eta=float(_eta)


    def nodeUpdateRule(self, node, srcNetwork, dt):
        # Read original node state.
        srcState = node[1][self.STATE_ATTR_NAME]
        # By default we have not changed states, so set
        # the destination state to be the same as the source state.
        dstState = srcState

        # Start out with a dictionary of zero neighbors in each state.
        nNSt = dict(zip(self.nodeStateIds,[0]*len(self.nodeStateIds)))
        # Calculate the actual numbers and update dictionary.
        nNSt.update(attributeCount(neighbors_data_iter(srcNetwork, node[0]),
                                   self.STATE_ATTR_NAME))

        # Pick a random number.
        eventp = numpy.random.random_sample()

        # Go through each state name, and chose an action.

        if srcState == 'I':
            stay_prob=numpy.power((1-self._lambda*dt),nNSt['S'])
            if eventp<1-stay_prob:
                if numpy.random.random_sample()<self._beta:
                    dstState = 'R'
                else:
                    dstState = 'S'
        elif srcState == 'S':
            stay_prob=numpy.power((1-self._lambda*self._alpha*dt),nNSt['S'])*(1-self._delta*dt)
            if eventp<1-stay_prob:
                dstState = 'R'
        elif srcState == 'R':
            stay_prob=numpy.power((1-self._lambda*(1-self._eta)*dt),nNSt['S'])*(1-self._xi*dt)
            if eventp<1-stay_prob:
                dstState = 'S'

        node[1][self.STATE_ATTR_NAME] = dstState

        return node


#        if nNSt['S']>0 and eventp < 1-numpy.power((1-self._lambda*dt),nNSt['S']):
#            if srcState == 'I':
#                if numpy.random.random_sample()<self._beta:
#                    dstState = 'R'
#                else:
#                    dstState = 'S'
#            elif srcState == 'S':
#                if numpy.random.random_sample()<self._alpha:
#                    dstState = 'R'
#            elif srcState == 'R':
#                if numpy.random.random_sample()<(1-self._eta):
#                    dstState = 'S'
#        if srcState == 'S' and eventp < self._delta*dt:
#            dstState = 'R'
#        if srcState == 'R' and eventp < self._xi*dt:
#            dstState = 'S'