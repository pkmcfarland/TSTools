# all blank lines and all lines starting with # will be skipped
# use 1 (on) and 0 (off) to toggle functionality

# Flags for type of inversion to perform:

IM: basin           # inversion method: linear = weighted least squares
                    #                   basin = basinhopping (must also include LM flat)

LM: nelder          # local-minimum finder: nelder = Nelder-Mead

# Flags for parameters to estimate for components: x1 x2 x3

POS: 1 1 1          # position at t_0
VEL: 1 1 1          # linear velocity
AN: 1 1 1           # seasonal signal with annual period
SA: 1 1 1           # seasonal signal with semi-annual period

# Flag for break information file

BF: ./earthQuakes.txt       # path and file name of break file can be
                            # provided multiple times to include multiple files
BF: ./equipmentChanges.txt
