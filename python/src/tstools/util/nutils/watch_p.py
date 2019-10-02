#!/usr/bin/env python3

__all__ = ["watch"]

def watch(var):
    import inspect

    st = inspect.stack()[1]
    ind0 = st[4][0].index("(")
    indf = st[4][0].rindex(")")
    var_name = st[4][0][ind0+1:indf]
    fn = st[1]
    line = st[2]
    func = st[3]

    if type(var) == type(""):
        var = '"%s"'%(str(var))

    print()
    print("DBG: {fn}:{line}:{func} {var_name} = {var}".format(**locals()))
