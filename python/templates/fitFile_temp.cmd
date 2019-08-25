
# General rules for constructing file:
# 1.) all blank lines and all lines starting with # will be skipped
# 2.) line must start with 2-char flag followed by colon
# 3.) all flag arguments must be on same line as flag
# 4.) flags can be UPPER or lower 
# 5.) white space separates flag from arguments and arguments from each other, 
#     can have as much white space as you like
# 6.) the only mandatory flag is IM

# Rules for parameter estimation flags:
# 7.) use 999 to include as a paramter to be estimated or 0 to not include the
#     parameter at all. Any other value will fix the parameter in the inversion
#     to the value provided.

#     E.g.: the line below will tell TSTools to set the east velocity to 
#           2.3 mm/yr, the north velocity to 1.2 mm/yr and to estimate the up 
#           velocity.
#           VE: 0.0023 0.0012 999
#
# 7.) not including a parameter estimation flag is equivalent to setting all
#     of that flag's associated arguments to 0

# Flags for type of inversion to perform:

IM: basin           # (I)nversion (M)ethod: linear = weighted least squares
                    #                       basin = basinhopping (must also include LM flat)
                    #                       gensyn = do not perform any inversion, 
                    #                                use given parameters to create
                    #                                a synthetic time series

LM: nelder          # (L)ocal-(M)inimum finder, only necessary if IM set to 'basin': 
                    #                       nelder = Nelder-Mead

# Flags for parameters to estimate for each component:
# Note - if coord.s in dEdNdU x1 = E, x2 = N, x3 = U
#        if coord.s in dXdYdZ x1 = X, x2 = Y, x3 = Z

#   x1  x2  x3
DC: 999 999 999  # (DC)-offset term (i.e. pos at t=0) (m)
VE: 999 999 999  # linear (VE)locity (m/yr)
AN: 999 999 999  # magnitude of seasonal signal with (AN)nual period (m)
SA: 999 999 999  # magnitude of seasonal signal with (S)emi-(A)nnual period (m)
O2:   0   0   0  # magnitude of terms of (O)rder (2) in time
O3:   0   0   0  # magnitude of terms of (O)rder (3) in time
O4:   0   0   0  # magnitude of terms of (O)rder (4) in time
