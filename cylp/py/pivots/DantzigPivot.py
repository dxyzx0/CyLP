'''
As a part of ``cylp.python.pivots`` it implements Dantzig's
Classical Simplex pivot rule. Although it already exists in CLP,
for testing purposes we implement one in Python.
'''

import sys
import numpy as np
from operator import itemgetter
from random import shuffle
from math import floor
from .PivotPythonBase import PivotPythonBase

import os
import pickle
import pandas as pd


def inv_basis_code(c):
    if c == 0:
        return 'isFree'
    elif c == 1:
        return 'basic'
    elif c == 2:
        return 'atUpperBound'
    elif c == 3:
        return 'atLowerBound'
    elif c == 4:
        return 'superBasic'
    elif c == 5:
        return 'isFixed'
    else:
        raise ValueError('Invalid basis code')

class DantzigPivot(PivotPythonBase):
    '''
    Dantzig's pivot rule implementation.

    **Usage**

    >>> from cylp.cy import CyClpSimplex
    >>> from cylp.py.pivots import DantzigPivot
    >>> from cylp.py.pivots.DantzigPivot import getMpsExample
    >>> # Get the path to a sample mps file
    >>> f = getMpsExample()
    >>> s = CyClpSimplex()
    >>> s.readMps(f)  # Returns 0 if OK
    0
    >>> pivot = DantzigPivot(s)
    >>> s.setPivotMethod(pivot)
    >>> s.primal()
    'optimal'
    >>> round(s.objectiveValue, 5)
    2520.57174

    '''

    def add_row(self):
        # add row to dataframes
        s = self.clpModel
        i = s.iteration

        if i == 0:
            # self.basis.to_csv(os.path.join(path, 'basis.csv'), index=False)
            with open(os.path.join(self.path, 'data.pickle'), 'wb') as f:
                pickle.dump((self.nCols,
                             self.nRows,
                             self.varLower,
                             self.varUpper,
                             self.rowLower,
                             self.rowUpper,
                             self.c,
                             self.A
                             ), f)
        else:
            # self.basis.loc[len(self.basis)] = np.concatenate(([i], list(map(inv_basis_code, np.concatenate(s.getBasisStatus())))))
            stats = pd.DataFrame([[i, s.sequenceIn(), s.getPivotVariable()[s.pivotRow()], s.sumPrimalInfeasibilities,
                     s.numberPrimalInfeasibilities, s.sumDualInfeasibilities, s.numberDualInfeasibilities]], columns=['iter'] + ['in_var', 'out_var', 'sum_primal_inf', 'n_primal_inf', 'n_dual_inf', 'sum_dual_inf'])
            # self.stats[len(self.stats)] = stats
            # rc = pd.DataFrame([np.concatenate(([i], s.reducedCosts))], columns=['iter'] + [f'var_{i}' for i in range(self.nCols)] + [f'slack_{i}' for i in range(self.nCols, self.dim)])
            stats.to_csv(os.path.join(self.path, 'stats.csv'), mode='a', index=False, header=(i == 0))
            # rc.to_csv(os.path.join(self.path, 'rc.csv'), mode='a', index=False, header=False)

    def init_attr(self, s, prob_name):
        self.prob = prob_name
        self.nCols = s.nCols
        self.nRows = s.nRows
        self.varLower = s.variablesLower
        self.varUpper = s.variablesUpper
        self.rowLower = s.constraintsLower
        self.rowUpper = s.constraintsUpper
        self.c = s.objective
        self.A = s.coefMatrix

        self.path = "output/{}/{}/".format(self.prob, "p_dantzig")
        os.makedirs(self.path, exist_ok=True)

        self.stats = {}
        # self.basis = pd.DataFrame(columns=['iter'] + [f'var_{i}' for i in range(self.nCols)] +[f'slack_{i}' for i in range(self.nCols, self.dim)])
        self.rc = {}

    def __init__(self, clpModel, prob_name):
        self.dim = clpModel.nRows + clpModel.nCols
        self.clpModel = clpModel

        self.init_attr(self.clpModel, prob_name)

    def pivotColumn(self, updates, spareRow1, spareRow2, spareCol1, spareCol2):
        'Finds the variable with the best reduced cost and returns its index'
        self.add_row()

        s = self.clpModel

        # Update the reduced costs, for both the original and the slack variables
        self.updateReducedCosts(updates, spareRow1, spareRow2, spareCol1, spareCol2)

        rc = s.reducedCosts
        tol = s.dualTolerance

        indicesToConsider = np.where(s.varNotFlagged & s.varNotFixed &
                                     s.varNotBasic &
                                     (((rc > tol) & s.varIsAtUpperBound) |
                                     ((rc < -tol) & s.varIsAtLowerBound) |
                                     s.varIsFree))[0]

        #freeVarInds = np.where(s.varIsFree)
        #rc[freeVarInds] *= 10

        rc2 = np.abs(rc[indicesToConsider])

        checkFree = True
        #rc2[np.where((status & 7 == 4) | (status & 7 == 0))] *= 10
        if rc2.shape[0] > 0:
            if checkFree:
                w = np.where(s.varIsFree)[0]
                if w.shape[0] > 0:
                    ind = s.argWeightedMax(rc2, indicesToConsider, 1, w)
                else:
                    ind = np.argmax(rc2)
            else:
                    ind = np.argmax(rc2)
            #del rc2
            return  indicesToConsider[ind]
        return -1

    def saveWeights(self, model, mode):
        self.clpModel = model

    def isPivotAcceptable(self):
        return True


def getMpsExample():
    import os
    import inspect
    cylpDir = os.environ['CYLP_SOURCE_DIR']
    return os.path.join(cylpDir, 'cylp', 'input', 'p0033.mps')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        import doctest
        doctest.testmod()
    else:
        from cylp.cy import CyClpSimplex
        from cylp.py.pivots import DantzigPivot
        s = CyClpSimplex()
        s.readMps(sys.argv[1])
        pivot = DantzigPivot(s, sys.argv[1])
        s.setPivotMethod(pivot)
        s.primal()
