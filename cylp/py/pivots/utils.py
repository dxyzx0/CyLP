import os
import pickle
import pandas as pd


def add_row(s, path):
    # add row to dataframes
    i = s.iteration

    if i == 0:
        # self.basis.to_csv(os.path.join(path, 'basis.csv'), index=False)
        with open(os.path.join(path, 'data.pickle'), 'wb') as f:
            pickle.dump((s.nCols,
                         s.nRows,
                         s.variablesLower,
                         s.variablesUpper,
                         s.constraintsLower,
                         s.constraintsUpper,
                         s.objective,
                         s.coefMatrix
                         ), f)
    else:
        # self.basis.loc[len(self.basis)] = np.concatenate(([i], list(map(inv_basis_code, np.concatenate(s.getBasisStatus())))))
        stats = pd.DataFrame([[i, s.sequenceIn(), s.sequenceOut(), s.sumPrimalInfeasibilities,
                               s.numberPrimalInfeasibilities, s.sumDualInfeasibilities,
                               s.numberDualInfeasibilities]],
                             columns=['iter'] + ['in_var', 'out_var', 'sum_primal_inf', 'n_primal_inf',
                                                 'n_dual_inf', 'sum_dual_inf'])
        # self.stats[len(self.stats)] = stats
        # rc = pd.DataFrame([np.concatenate(([i], s.reducedCosts))], columns=['iter'] + [f'var_{i}' for i in range(self.nCols)] + [f'slack_{i}' for i in range(self.nCols, self.dim)])
        stats.to_csv(os.path.join(path, 'stats.csv'), mode='a', index=False, header=(i <= 1))
        # rc.to_csv(os.path.join(self.path, 'rc.csv'), mode='a', index=False, header=False)


def init_attr(self, s, prefix, prob_name):
    self.prob = prob_name
    self.nCols = s.nCols
    self.nRows = s.nRows
    self.varLower = s.variablesLower
    self.varUpper = s.variablesUpper
    self.rowLower = s.constraintsLower
    self.rowUpper = s.constraintsUpper
    self.c = s.objective
    self.A = s.coefMatrix

    self.path = f"{prefix}/{self.prob}/{self.__class__.__name__}/"
    os.makedirs(self.path)
