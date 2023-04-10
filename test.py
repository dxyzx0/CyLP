from cylp.cy import CyClpSimplex
import os


if __name__ == "__main__":
    # s = CyClpSimplex()
    # s.readMps('cylp_/input/netlib/adlittle.mps')
    #
    # s.initialSolve()
    #
    # round(s.objectiveValue, 3)

    from cylp.cy import CyClpSimplex
    from cylp.py.pivots import DantzigPivot, PositiveEdgePivot, LIFOPivot, MostFrequentPivot, PositiveEdgeWolfePivot, WolfePivot
    # Get the path to a sample mps file

    netlib = "cylp/input/netlib"
    for mps in os.listdir(netlib):
        if ".mps" not in mps:
            print("Skipping", mps)
            continue
        for pivot in [DantzigPivot, PositiveEdgePivot, LIFOPivot, MostFrequentPivot, PositiveEdgeWolfePivot, WolfePivot]:
            f = os.path.join(netlib, mps)
            s = CyClpSimplex()
            s.readMps(f)  # Returns 0 if OK
            pivot = DantzigPivot(s, mps.split(".")[0])
            # pivot = PositiveEdgePivot(s)
            s.setPivotMethod(pivot)
            s.primal()
            round(s.objectiveValue, 5)
