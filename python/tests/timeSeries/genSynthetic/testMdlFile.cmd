
# General rules for constructing file:
# 1.) all blank lines and all lines starting with # will be skipped
# 2.) line must start with 2-char flag followed by colon
# 3.) all flag args must be on same line as flag
# 4.) flags can be UPPER or lower 
# 5.) white space separates flag from args, can have as much white
#     space as you like

# Rules for parameter est flags:
# 6.) use 1 (on) and 0 (off) to toggle functionality

# Flags for type of inversion to perform:

IM: basin           # (I)nversion (M)ethod: linear = weighted least squares
                    #                       basin = basinhopping (must also include LM flat)

LM: nelder          # (L)ocal-(M)inimum finder, only necessary if IM set to 'basin': 
                    #                       nelder = Nelder-Mead

# Flags for parameters to estimate for each component:
# Note - if coord.s in dEdNdU x1 = E, x2 = N, x3 = U
#        if coord.s in dXdYdZ x1 = X, x2 = Y, x3 = Z

#   x1  x2  x3
DC:  1   1   1      # (DC)-offset term (i.e. pos at t=0)
VE:  1   1   1      # linear (VE)locity
AN:  1   1   1      # seasonal signal with (AN)nual period
SA:  1   1   1      # seasonal signal with (S)emi-(A)nnual period
PO:  0   0   0      # 4th order (PO)lynomial **NOT YET FUNCTIONAL**
