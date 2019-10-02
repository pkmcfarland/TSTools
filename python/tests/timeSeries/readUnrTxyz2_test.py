import sys

sys.path.append("./src")
from tstools import timeSeries as ts


def test_readUnrTxyz2():
    series = ts.TimeSeries()
    series.readUnrTxyz2("./tests/timeSeries/AREQ.IGS08.txyz2")

    assert series.time.size == 7759
    assert series.time.shape == (7759,)
    assert series.time[0] == 1996.0

    assert series.pos.size == (7759 * 3)
    assert series.pos.shape == (3, 7759)

    assert series.sig.size == (7759 * 3)
    assert series.sig.shape == (3, 7759)

    assert series.corr.size == (7759 * 3)
    assert series.corr.shape == (3, 7759)
