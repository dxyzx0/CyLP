from cylp.cy import CyClpSimplex

if __name__ == "__main__":
    # s = CyClpSimplex()
    # s.readMps('cylp_/input/netlib/adlittle.mps')
    #
    # s.initialSolve()
    #
    # round(s.objectiveValue, 3)

    from cylp.cy import CyClpSimplex
    from cylp.py.pivots import DantzigPivot, PositiveEdgePivot
    # Get the path to a sample mps file
    f = "cylp/input/netlib/25fv47.mps"
    s = CyClpSimplex()
    s.readMps(f)  # Returns 0 if OK
    # pivot = DantzigPivot(s)
    pivot = PositiveEdgePivot(s)
    s.setPivotMethod(pivot)
    s.primal()
    round(s.objectiveValue, 5)
