
# General rules for constructing file:
# 1.) all blank lines and all lines starting with # will be skipped
# 2.) columns are white-space separated, amount of white space does not matter
# 3.) events do not need to be in chronological order
# 4.) start new break record with +, end break record with -
# 5.) record values other than those associated with time of break can have 
#     either:
#     999 => include parameter in estimation
#       0 => do not include this parameter at all
#     any other value assigns that value to the parameter and fixes it in the
#     inversion
# 5.) break record can have either 1 or 7 lines
# 6.) if break record has only one line the columns for the line are:
#     
#     01 +        start new record
#     02 YYYY     4-digit year    (int)
#     03 MM       2-digit month   (int)
#     04 DD       2-digit day     (int)
#     05 HH       2-digit hour    (int)
#     07 MN       2-digit minute  (int)
#     08 SS.SS    decimal seconds (float)
#     09          magnitude of x1 offset (m)
#     10          magniutde of x2 offset (m)
#     11          magnitude of x3 offset (m)
#
# 7.) if break record has 7 lines the format for the record is:
#     line #1:
#     same as single line record but do not include end of record symbol (-)
#
#     line #2:
#     01          magnitude of first exp x1 term (m)
#     02          magnitude of second exp x1 term (m)
#     03          magnitude of third exp x1 term (m)
#     04          relaxation time of first exp x1 term (yrs)
#     05          relaxation time of second exp x1 term (yrs)
#     06          relaxation time of third exp x1 term (yrs)
#
#     line #3:
#     same as line #2 but for x2
#
#     line #4:
#     same as line #2 but for x3
#
#     line #5:
#     01          magnitude of ln x1 term (m)
#     02          relaxation time of ln x1 term (yrs)
#
#     line #6:
#     same as line #5 but for x2
#
#     line #7:
#     same as line #5 bur for x3
#
#     line #8:
#     01 -        end record
       

#                          ___Offset____                     # Description of event
# YYYY MM DD HH MN SS.SS   x1_  x2_  x3_                    
+ 2001 11 14 15 40 53.00   999  999  999                     # Mw 7.7 Tocopilla EQ; estimate offsets
#                          __________ExpTerms___________     # and three logarithmic terms
#                          mag1 mag2 mag3 tau1 tau2 tau3   
#                          _____________x1______________
                            999  999  999  999  999  999 
#                          _____________x2______________
                            999  999  999  999  999  999  
#                          _____________x3______________
                            999  999  999  999  999  999
#                          _________LnTerms_____________
#                           mag  tau
#                          ____x1___
                              0    0
#                          ____x2___
                              0    0
#                          ____x3___ 
                              0    0 
- any text can follow end-record symbol

+ 2003  3  1 12  0  0.00  999  999  999                      # Antenna change topcon -> trimble zephyr II
- end-record symbol can be below or last line of record      # estimate offsets only

+ 2010  2 27  6 34 23.00 0.14 0.12 0.07                      # Mw 8.8 Maule EQ, initial offsets known to be
                          999  999    0  999  999   0        # 14 cm east, 12 cm north, and 7 cm up. estimate
                          999  999    0  999  999   0        # two post-seismic terms and 0 logarithmic terms
                          999  999    0  999  999   0    
                            0    0  
                            0    0   
                            0    0   
-
