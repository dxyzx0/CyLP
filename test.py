from cylp.cy import CyClpSimplex
import os
from datetime import datetime


if __name__ == "__main__":
    # s = CyClpSimplex()
    # s.readMps('cylp_/input/netlib/adlittle.mps')
    #
    # s.initialSolve()
    #
    # round(s.objectiveValue, 3)

    from cylp.cy import CyClpSimplex
    from cylp.py.pivots import DantzigPivot, PositiveEdgePivot, LIFOPivot, MostFrequentPivot, PositiveEdgeWolfePivot, \
        WolfePivot

    # Get the path to a sample mps file

    # prefix is output + time stamp as folder name
    prefix = f"output/{datetime.now().strftime('%Y.%m.%d_%H_%M_%S')}"
    netlib = "cylp/input/netlib"
    for mps in sorted(os.listdir(netlib)):
        if ".mps" not in mps:
            print("Skipping", mps)
            continue

        # FIXME: bug
        if mps in ("d2q06c.mps", "dfl001.mps"):
            continue

        f = os.path.join(netlib, mps)
        for pivot in [
            DantzigPivot,
            PositiveEdgePivot,
            # LIFOPivot,  # too slow
            # MostFrequentPivot,  # too slow
        ]:
            s = CyClpSimplex()
            s.readMps(f)  # Returns 0 if OK
            pt = pivot(s, prefix, mps.split(".")[0])
            s.setPivotMethod(pt)
            s.primal()
            round(s.objectiveValue, 5)
