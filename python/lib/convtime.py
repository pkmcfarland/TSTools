#!/usr/bin/env python3

"""
Module with common time conversions.

Product of: 
U.S. Nat.'l Geodetic Survey / Nat.'l Oceanic Atmospheric Admin.
1315 East-West Hwy.
Silver Spring, MD, 20910

Author(s):
Sungpil Yoon

Contact:
sungpil.yoon@noaa.gov

As required by 17 U.S.C. § 403, third parties producing copyrighted works consisting predominantly 
of the material appearing in NGS Web pages must provide notice with such work(s) identifying the NGS 
material incorporated and stating that such material is not subject to copyright protection.
"""

from numpy.testing import assert_allclose, assert_equal

import math
import sys

from nutils import watch, msg_err
import datetime as dt

__all__ = ["DeltaTime", "PreciseTime", "convtime", "format_time", "last_doy"]
__all__.extend(["mm_to_month", "yy_to_yyyy", "yyyy_to_yy"])

format_list = ["mjd", "mjd2", "mjd3", "jd", "cal", "doy", "gps", "gps2",
        "sec", "year", "datetime"]

class PreciseTime:
    def __init__(self, fmt, val):
        """Create PreciseTime object

        fmt : format
        val : list of values

        Note:
            * For the list of available formats and how to put values,
              please refer convtime help message
        """

        self._val = convtime(fmt, "mjd2", val)
        self._prec = 1e-12
        
    def get(self, fmt, aprx=99):
        return convtime("mjd2", fmt, self._val, aprx=aprx)

    def to_str(self, fmt):
        return format_time(fmt, self)

    def __str__(self):
        return "PT:{}".format(self.get("cal"))

    def __repr__(self):
        return self.__str__()

    def __sub__(self, other):
        """
        >>> pe1 = PreciseTime("cal", [2017, 1, 1, 0, 0, 0])
        >>> pe2 = PreciseTime("cal", [2017, 1, 2, 0, 0, 0.1])
        >>> dt = pe2 - pe1

        >>> dt.get("sec")
        86400.1

        >>> dt.get("day")
        1.0000011574074075

        >>> dt = pe1 - pe2

        >>> dt.get("sec")
        -86400.1
        """

        assert type(other) is PreciseTime
        
        ret = diff_mjd2(self.get("mjd2"), other.get("mjd2"))
        return DeltaTime("day", ret)

    def __add__(self, other):
        """
        >>> pe1 = PreciseTime("cal", [2017, 1, 1, 0, 0, 0])
        >>> dt = DeltaTime("sec", 86400.1)
        >>> pe2 = pe1 + dt

        >>> pe2.to_str("[YYYY]/[MM]/[DD] [HH]:[MN]:[SS3]")
        '2017/01/02 00:00:00.100'
        """

        assert type(other) is DeltaTime
        
        new_mjd2 = add_mjd2(self.get("mjd2"), other.get("day"))
        return PreciseTime("mjd2", new_mjd2)
        
    def __lt__(self, other):
        if self.get("cal", self._prec) < other.get("cal", self._prec):
            return True
        else:
            return False
            
    def __le__(self, other):
        if self.get("cal", self._prec) <= other.get("cal", self._prec):
            return True
        else:
            return False
            
    def __eq__(self, other):
        if self.get("cal", self._prec) == other.get("cal", self._prec):
            return True
        else:
            return False
            
    def __ne__(self, other):
        if self.get("cal", self._prec) != other.get("cal", self._prec):
            return True
        else:
            return False
            
    def __gt__(self, other):
        if self.get("cal", self._prec) > other.get("cal", self._prec):
            return True
        else:
            return False
            
    def __ge__(self, other):
        if self.get("cal", self._prec) >= other.get("cal", self._prec):
            return True
        else:
            return False


def test1():

    time = PreciseTime("mjd2", [57022, 0])
    dt = DeltaTime("day", 0.2)
    new_time = time + dt
    assert_allclose(new_time.get("mjd2"), [57022, 0.2], rtol=1e-12)

    time = PreciseTime("mjd2", [57022, 0])
    dt = DeltaTime("day", -0.2)
    new_time = time + dt
    assert_allclose(new_time.get("mjd2"), [57021, 0.8], rtol=1e-12)

    time = PreciseTime("mjd2", [57022, 0])
    time2 = PreciseTime("mjd2", [57022, 0.4])
    dt = time - time2
    assert_allclose(dt.get("day"), -0.4, rtol=1e-12)

    time = PreciseTime("mjd2", [57022, 0])
    time2 = PreciseTime("mjd2", [57023, 0.4])
    dt = time - time2
    assert_allclose(dt.get("day"), -1.4, rtol=1e-12)

    dt = time2 - time
    assert_allclose(dt.get("day"), 1.4, rtol=1e-12)

    # PreciseTime should have better than pico second resolution

    rtol = 1e-12

    time = PreciseTime("mjd2", [57022, 0])
    dt = DeltaTime("sec", 1e-12)
    time2 = time + dt
    dt2 = time2 - time
    assert_allclose(dt2.get("sec"), dt.get("sec"), rtol=rtol)

    time = PreciseTime("cal", [2015, 10, 1, 0, 0, 0])
    time2 = PreciseTime("cal", [2015, 10, 1, 0, 0, 1e-12])
    dt = time2 - time
    assert_allclose(dt.get("sec"), 1e-12, rtol=rtol)

def test2():

    got = yy_to_yyyy(15)
    assert_equal(got, 2015)

    got = yy_to_yyyy(90)
    assert_equal(got, 1990)

    got = yy_to_yyyy(00)
    assert_equal(got, 2000)

    got = yyyy_to_yy(2015)
    assert_equal(got, 15)

    got = yyyy_to_yy(1990)
    assert_equal(got, 90)

    got = yyyy_to_yy(2000)
    assert_equal(got, 0)

def test3():

    actual = convtime("mjd", "mjd", 57022)
    assert_equal(actual, 57022.0)
    
    actual = convtime("mjd2", "mjd2", [57022, 0.3])
    assert_equal(actual, [57022, 0.3])
    
    actual = convtime("mjd3", "mjd3", [57022, 3600.000000000001])
    assert_equal(actual, [57022, 3600.000000000001])
    
    actual = convtime("jd", "jd", 2457022.5)
    assert_equal(actual, 2457022.5)
    
    actual = convtime("cal", "cal", [2015, 1, 1, 0, 0, 1.000000000001])
    assert_equal(actual, [2015, 1, 1, 0, 0, 1.000000000001])
    
    actual = convtime("doy", "doy", [2015, 40, 0, 0, 1.000000000001])
    assert_equal(actual, [2015, 40, 0, 0, 1.000000000001])
    
    actual = convtime("gps", "gps", [1825, 259200.0])
    assert_equal(actual, [1825, 259200.0])
    
    actual = convtime("gps", "gps", [1700, 400000.000000001])
    assert_equal(actual, [1700, 400000.000000001])

    actual = convtime("gps2", "gps2", [1825, 3, 0, 0, 1.000000000001])
    assert_equal(actual, [1825, 3, 0, 0, 1.000000000001])
    

def test4():

    actual = convtime("mjd", "mjd", 57022)
    assert actual == 57022.0
    
    actual = convtime("mjd2", "mjd2", [57022, 0.3])
    assert actual == [57022, 0.3]
    
    actual = convtime("mjd3", "mjd3", [57022, 3600.000000000001])
    assert actual == [57022, 3600.000000000001]
    
    actual = convtime("jd", "jd", 2457022.5)
    assert actual == 2457022.5
    
    actual = convtime("cal", "cal", [2015, 1, 1, 0, 0, 1.000000000001])
    assert actual == [2015, 1, 1, 0, 0, 1.000000000001]
    
    actual = convtime("doy", "doy", [2015, 40, 0, 0, 1.000000000001])
    assert actual == [2015, 40, 0, 0, 1.000000000001]
    
    actual = convtime("gps", "gps", [1825, 259200.0])
    assert actual == [1825, 259200.0]
    
    actual = convtime("gps2", "gps2", [1825, 3, 0, 0, 1.000000000001])
    assert actual ==  [1825, 3, 0, 0, 1.000000000001]

    actual = convtime("gps", "gps", [1700, 400000.000000001])
    assert actual == [1700, 400000.000000001]

    actual = days_to_hmsm(0.1)
    assert actual == (2, 24, 0, 1.2789769243681803e-06)


class DeltaTime:
    """Class to be used with addition (+) and subtraction (-) of PreciseTime
    """

    def __init__(self, fmt, val):
        if fmt == "day":
            self._val = val
            
        elif fmt == "sec":
            self._val = val/86400

        elif fmt == "year":
            self._val = val*365.25

        else:
            err_msg("Not defined")
            
    def get(self, fmt):
        if fmt == "day":
            ret = self._val
            
        elif fmt == "sec":
            ret = self._val*86400

        elif fmt == "year":
            ret = self._val/365.25
            
        return ret
        
    def __str__(self):
        return "{}".format(self.get("sec"))
 
# Note: The Python datetime module assumes an infinitely valid Gregorian calendar.
#       The Gregorian calendar took effect after 10-15-1582 and the dates 10-05 through
#       10-14-1582 never occurred. Python datetime objects will produce incorrect
#       time deltas if one date is from before 10-15-1582.
 

def yy_to_yyyy(yy):
    """
    >>> yy_to_yyyy(15)
    2015
    >>> yy_to_yyyy(90)
    1990
    >>> yy_to_yyyy(00)
    2000
    """

    if yy < 80:
        yyyy = yy + 2000
    else:
        yyyy = yy + 1900
    return int(yyyy)

    
   
def yyyy_to_yy(yyyy):
    """
    >>> yyyy_to_yy(2015)
    15
    >>> yyyy_to_yy(1990)
    90
    >>> yyyy_to_yy(2000)
    0
    """

    if yyyy >= 2000:
        yy = yyyy - 2000
    else:
        yy = yyyy - 1900
    return int(yy)

def diff_mjd2(mjd21, mjd22):
    """
    >>> diff_mjd2((57022, 0.2), (57021, 0.8))
    0.3999999999999999
    >>> diff_mjd2((57021, 0.8), (57022, 0.2))
    -0.3999999999999999
    """

    tmp1 = mjd21[0] - mjd22[0]
    tmp2 = mjd21[1] - mjd22[1]
    
    return tmp1 + tmp2

def add_mjd2(mjd2, day):
    """
    >>> add_mjd2([57022, 0.2], 0.9)
    [57023, 0.10000000000000009]
    >>> add_mjd2([57022, 0.2], -0.5)
    [57021, 0.7]
    """
    
    new_mjd2 = [mjd2[0], mjd2[1] + day]
    new_mjd2 = clean_mjd2(new_mjd2)
    return new_mjd2

def clean_mjd2(mjd2):
    """
    >>> clean_mjd2([57022, 0.2])
    [57022, 0.2]
    >>> clean_mjd2([57022, 1.2])
    [57023, 0.19999999999999996]
    >>> clean_mjd2([57022, 10.2])
    [57032, 0.1999999999999993]
    >>> clean_mjd2([57022, -0.2])
    [57021, 0.8]
    >>> clean_mjd2([57022, -1.2])
    [57020, 0.8]
    """

    if mjd2[1] >= 0:    
        tmp = int(mjd2[1])
    else:
        tmp = int(mjd2[1]) - 1
        
    new_mjd2 = [None, None]
    new_mjd2[0] = mjd2[0] + tmp
    new_mjd2[1] = mjd2[1] - tmp
        
    return new_mjd2
    
def mm_to_month(mm):
    """
    >>> mm_to_month(1)
    'January'
    """

    data = ["January", "February", "March", "April", "May", "June", \
            "July", "August", "September", "October", "November", "December"]

    ret = data[mm - 1]

    return ret

def test_format_time():
    ret = format_time("[MJD0]", PreciseTime("cal", [2019, 2, 11, 0, 0, 0]))
    assert ret == "58525"

    ret = format_time("[MJD2]", PreciseTime("cal", [2019, 2, 11, 0, 0, 0]))
    assert ret == "58525.00"

    ret = format_time("[MJD5]", PreciseTime("cal", [2019, 2, 11, 0, 0, 1e-9]))
    assert ret == "58525.00000"

    pe = PreciseTime("cal", [2019, 2, 11, 0, 0, 1e-9])

    ret = format_time("[YYYY]-[DDD] [HH]:[MN]:[SS6]", pe)
    assert ret == "2019-042 00:00:00.000000"

    ret = format_time("[YYYY]-[DDD] [HH]:[MN]:[SS9]", pe)
    assert ret == "2019-042 00:00:00.000000001"

    pe = PreciseTime("cal", [2019, 2, 11, 23, 59, 60 - 1e-9])

    ret = format_time("[YYYY]-[DDD] [HH]:[MN]:[SS9]", pe)
    assert ret == "2019-042 23:59:59.999999999"

    ret = format_time("[YYYY]-[DDD] [HH]:[MN]:[SS6]", pe)
    assert ret == "2019-043 00:00:00.000000"


def convtime(ifmt, ofmt, data, aprx=99):
    """Convert time formats

    >>> convtime("mjd", "mjd", 57022)
    57022.0

    >>> convtime("mjd2", "mjd2", [57022, 0.3])
    [57022, 0.3]

    >>> convtime("mjd3", "mjd3", [57022, 3600.000000000001])
    [57022, 3600.000000000001]

    >>> convtime("jd", "jd", 2457022.5)
    2457022.5

    >>> convtime("cal", "cal", [2015, 1, 1, 0, 0, 1.000000000001])
    [2015, 1, 1, 0, 0, 1.000000000001]

    >>> convtime("doy", "doy", [2015, 40, 0, 0, 1.000000000001])
    [2015, 40, 0, 0, 1.000000000001]

    >>> convtime("gps", "gps", [1825, 259200.0])
    [1825, 259200.0]

    >>> convtime("gps2", "gps2", [1825, 3, 0, 0, 1.000000000001])
    [1825, 3, 0, 0, 1.000000000001]

    >>> convtime("sec", "sec", 100000.000001)
    100000.000001

    >>> convtime("year", "year", 2017.000000000001)
    2017.000000000001
    """

    # input processing
    if ifmt == "mjd":
        mjd2 = mjd_to_mjd2(data)

    elif ifmt == "mjd2":
        mjd2 = data

    elif ifmt == "mjd3":
        mjd2 = mjd3_to_mjd2(data)

    elif ifmt == "jd":
        mjd2 = jd_to_mjd2(data)

    elif ifmt == "cal":
        mjd2 = cal_to_mjd2(data)

    elif ifmt == "gps":
        mjd2 = gps_to_mjd2(data)

    elif ifmt == "gps2":
        mjd2 = gps2_to_mjd2(data)

    elif ifmt == "doy":
        mjd2 = doy_to_mjd2(data)

    elif ifmt == "datetime":
        mjd2 = datetime_to_mjd2(data)

    elif ifmt == "sec":
        mjd2 = sec_to_mjd2(data)
      
    elif ifmt == "year":
        mjd2 = year_to_mjd2(data)

    # output processing
    if ofmt == "mjd":
        ret = mjd2_to_mjd(mjd2)

    elif ofmt == "mjd2":
        ret = mjd2

    elif ofmt == "mjd3":
        ret = mjd2_to_mjd3(mjd2)

    elif ofmt == "jd":
        ret = mjd2_to_jd(mjd2)

    elif ofmt == "cal":
        ret = mjd2_to_cal(mjd2, aprx=aprx)

    elif ofmt == "gps":
        ret = mjd2_to_gps(mjd2)

    elif ofmt == "gps2":
        ret = mjd2_to_gps2(mjd2, aprx=aprx)

    elif ofmt == "doy":
        ret = mjd2_to_doy(mjd2, aprx=aprx)

    elif ofmt == "datetime":
        ret = mjd2_to_datetime(mjd2)

    elif ofmt == "sec":
        ret = mjd2_to_sec(mjd2)

    elif ofmt == "year":
        ret = mjd2_to_year(mjd2)

    return ret

def mjd_to_mjd2(mjd):
    mjd2 = [0, 0]
    mjd2[1], mjd2[0] = math.modf(mjd)
    return mjd2

def mjd3_to_mjd2(mjd3):
    mjd2 = [mjd3[0], 0]
    mjd2[1] = mjd3[1]/86400.
    return mjd2

def cal_to_mjd2(cal):
    jd = date_to_jd(cal[0], cal[1], cal[2])
    mjd = jd_to_mjd(jd)
    ss = int(cal[5])
    ms = (cal[5] - ss)*1e6 # convert to microseconds
    fd = hmsm_to_days(cal[3], cal[4], ss, ms)
    return [int(mjd), fd]

def jd_to_mjd2(jd):
    mjd = jd_to_mjd(jd)
    return int(mjd), mjd - int(mjd)

def gps_to_mjd2(gps):
    mjd0 = 44244 # 1980/1/6
    tmp1 = gps[0]*7
    tmp2 = int(gps[1]/86400.)
    mjd = tmp1 + mjd0 + tmp2
    fd = gps[1]/86400 - tmp2
    return [mjd, fd]

def gps2_to_mjd2(gps2):
    mjd2 = gps_to_mjd2([gps2[0], 0])
    mjd2[0] += int(gps2[1])
    ss = int(gps2[4])
    ms = (gps2[4] - int(gps2[4]))*1e6
    mjd2[1] = hmsm_to_days(gps2[2], gps2[3], ss, ms)
    return mjd2

def doy_to_mjd2(doy):
    yyyy = doy[0]
    mjd2 = cal_to_mjd2([yyyy, 1, 1, doy[2], doy[3], doy[4]])
    mjd2[0] += doy[1] - 1
    mjd2 = clean_mjd2(mjd2)

    return mjd2

def datetime_to_mjd2(datetime):
    yyyy = datetime.year
    month = datetime.month
    day = datetime.day
    hour = datetime.hour
    minute = datetime.minute
    second = datetime.second
    microsecond = datetime.microsecond

    cal = [yyyy, month, day, hour, minute, second+microsecond*1e-6]
    return cal_to_mjd2(cal)

def sec_to_mjd2(sec):
    datetime = dt.datetime.fromtimestamp(sec)
    return datetime_to_mjd2(datetime)

def year_to_mjd2(year):
    iyear = int(year)
    fyear = year - iyear

    num_days_in_year = convtime("cal", "doy", [iyear, 12, 31, 0, 0, 0])[1]
    day = num_days_in_year*fyear

    iday = int(day)
    fday = day - iday

    mjd2 = convtime("doy", "mjd2", [iyear, iday+1, 0, 0, 0])
    mjd2[1] = fday

    return mjd2

def mjd2_to_year(mjd2):
    doy = mjd2_to_doy(mjd2)
    iyear = doy[0]

    num_days_in_year = convtime("cal", "doy", [iyear, 12, 31, 0, 0, 0])[1]
    fyear = (doy[1] - 1 + mjd2[1])/num_days_in_year
    
    year = iyear + fyear

    return year

def mjd2_to_mjd(mjd2):
    mjd = mjd2[0] + mjd2[1]
    return mjd

def mjd2_to_mjd3(mjd2):
    mjd3 = [mjd2[0], 0]
    mjd3[1] = mjd2[1]*86400.
    return mjd3

def mjd2_to_jd(mjd2):
    jd = mjd_to_jd(mjd2[0] + mjd2[1])
    return jd

def mjd2_to_cal(mjd2, aprx=99):
    mjd = mjd2[0]

    hh, MM, ss, ms = days_to_hmsm(mjd2[1])
    ss = ss + ms*1e-6
    jd = mjd_to_jd(mjd)

    if aprx != 99:
        ss = round(ss/aprx)*aprx
        if ss == 60:
            ss = 0
            MM += 1
            if MM == 60:
                MM = 0
                hh += 1
                if hh == 24:
                    hh = 0
                    jd += 1

    yyyy, mm, dd = jd_to_date(jd)

    return [yyyy, mm, int(dd), hh, MM, ss]

def mjd2_to_gps(mjd2):
    gwkn, gwkd, hh, MM, ss = mjd2_to_gps2(mjd2)
    gsec = gwkd*86400 + hh*3600 + MM*60 + ss
    return [gwkn, gsec]

def mjd2_to_gps2(mjd2, aprx=99):
    yyyy, mm, dd, hh, mn, ss = mjd2_to_cal(mjd2, aprx)
    mjd2 = cal_to_mjd2([yyyy, mm, dd, 0, 0, 0])

    mjd0 = 44244 # 1980/1/6
    tmp1 = int((mjd2[0] - mjd0)/7.)
    tmp2 = mjd2[0] - mjd0 - 7*tmp1
    gwkn = tmp1
    gwkd = tmp2
    return [int(gwkn), int(gwkd), hh, mn, ss]

def mjd2_to_doy(mjd2, aprx=99):
    yyyy, mm, dd, hh, mn, ss = mjd2_to_cal(mjd2, aprx)
    mjd = cal_to_mjd2([yyyy, mm, dd, 0, 0, 0])[0]
    mjd0 = cal_to_mjd2([yyyy, 1, 1, 0, 0, 0])[0]
    ddd = mjd - mjd0 + 1

    return [yyyy, ddd, hh, mn, ss]

def mjd2_to_datetime(mjd2):
    cal = mjd2_to_cal(mjd2)
    sec = round(cal[-1])
    rem = cal[-1] - sec
    us = round(rem*1e6)
    datetime = dt.datetime(cal[0], cal[1], cal[2], cal[3], cal[4], sec, us)

    return datetime

def mjd2_to_sec(mjd2):
    datetime = mjd2_to_datetime(mjd2)
    return datetime.timestamp()

def mjd_to_jd(mjd):
    """
    Convert Modified Julian Day to Julian Day.
        
    Parameters
    ----------
    mjd : float
        Modified Julian Day
        
    Returns
    -------
    jd : float
        Julian Day
    
        
    """
    return mjd + 2400000.5

def jd_to_mjd(jd):
    """
    Convert Julian Day to Modified Julian Day
    
    Parameters
    ----------
    jd : float
        Julian Day
        
    Returns
    -------
    mjd : float
        Modified Julian Day
    
    """
    return jd - 2400000.5

def date_to_jd(year,month,day):
    """
    Convert a date to Julian Day.
    
    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
        4th ed., Duffet-Smith and Zwart, 2011.
    
    Parameters
    ----------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
        
    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.
    
    day : float
        Day, may contain fractional part.
    
    Returns
    -------
    jd : float
        Julian Day
        
    Examples
    --------
    Convert 6 a.m., February 17, 1985 to Julian Day
    
    >>> date_to_jd(1985,2,17.25)
    2446113.75
    
    """
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    
    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
        
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
        
    D = math.trunc(30.6001 * (monthp + 1))
    
    jd = B + C + D + day + 1720994.5
    
    return jd
    
def jd_to_date(jd):
    """
    Convert Julian Day to date.
    
    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
        4th ed., Duffet-Smith and Zwart, 2011.
    
    Parameters
    ----------
    jd : float
        Julian Day
        
    Returns
    -------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
        
    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.
    
    day : float
        Day, may contain fractional part.
        
    Examples
    --------
    Convert Julian Day 2446113.75 to year, month, and day.
    
    >>> jd_to_date(2446113.75)
    (1985, 2, 17.25)
    
    """
    jd = jd + 0.5
    
    F, I = math.modf(jd)
    I = int(I)
    
    A = math.trunc((I - 1867216.25)/36524.25)
    
    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I
        
    C = B + 1524
    
    D = math.trunc((C - 122.1) / 365.25)
    
    E = math.trunc(365.25 * D)
    
    G = math.trunc((C - E) / 30.6001)
    
    day = C - E + F - math.trunc(30.6001 * G)
    
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
        
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
        
    return year, month, day
    
def hmsm_to_days(hour=0,min=0,sec=0,micro=0):
    """
    Convert hours, minutes, seconds, and microseconds to fractional days.
    
    Parameters
    ----------
    hour : int, optional
        Hour number. Defaults to 0.
    
    min : int, optional
        Minute number. Defaults to 0.
    
    sec : int, optional
        Second number. Defaults to 0.
    
    micro : int, optional
        Microsecond number. Defaults to 0.
        
    Returns
    -------
    days : float
        Fractional days.
        
    Examples
    --------
    >>> hmsm_to_days(hour=6)
    0.25
    
    """
    days = sec + (micro / 1.e6)
    
    days = min + (days / 60.)
    
    days = hour + (days / 60.)
    
    return days / 24.
    
def days_to_hmsm(days):
    """
    Convert fractional days to hours, minutes, seconds, and microseconds.
    Precision beyond microseconds is rounded to the nearest microsecond.
    
    Parameters
    ----------
    days : float
        A fractional number of days. Must be less than 1.
        
    Returns
    -------
    hour : int
        Hour number.
    
    min : int
        Minute number.
    
    sec : int
        Second number.
    
    micro : int
        Microsecond number.
        
    Raises
    ------
    ValueError
        If `days` is >= 1.
        
    Examples
    --------
    >>> days_to_hmsm(0.1)
    (2, 24, 0, 1.2789769243681803e-06)
    
    """
    hours = days * 24.
    hours, hour = math.modf(hours)
    
    mins = hours * 60.
    mins, min = math.modf(mins)
    
    secs = mins * 60.
    secs, sec = math.modf(secs)
    
    #micro = round(secs * 1.e6)
    #return int(hour), int(min), int(sec), int(micro)
    
    micro = secs * 1.e6
    return int(hour), int(min), int(sec), micro
    
 
def datetime_to_jd(date):
    """
    Convert a `datetime.datetime` object to Julian Day.
    
    Parameters
    ----------
    date : `datetime.datetime` instance
    
    Returns
    -------
    jd : float
        Julian day.
        
    Examples
    --------
    #>>> d = dt.datetime(1985,2,17,6)  
    #>>> d
    #datetime.datetime(1985, 2, 17, 6, 0)
    #>>> jdutil.datetime_to_jd(d)
    #2446113.75
    
    """
    days = date.day + hmsm_to_days(date.hour,date.minute,date.second,date.microsecond)
    
    return date_to_jd(date.year,date.month,days)
    
    
def jd_to_datetime(jd):
    """
    Convert a Julian Day to an `jdutil.datetime` object.
    
    Parameters
    ----------
    jd : float
        Julian day.
        
    Returns
    -------
    dt : `jdutil.datetime` object
        `jdutil.datetime` equivalent of Julian day.
    
    Examples
    --------
    #>>> jd_to_datetime(2446113.75)
    #datetime(1985, 2, 17, 6, 0)
    
    """
    year, month, day = jd_to_date(jd)
    
    frac_days,day = math.modf(day)
    day = int(day)
    
    hour,min,sec,micro = days_to_hmsm(frac_days)
    #print(hour, min, sec, micro)
    
    return datetime(year,month,day,hour,min,sec,micro)
 
 
#def timedelta_to_days(td):
#    """
#    Convert a `datetime.timedelta` object to a total number of days.
#    
#    Parameters
#    ----------
#    td : `datetime.timedelta` instance
#    
#    Returns
#    -------
#    days : float
#        Total number of days in the `datetime.timedelta` object.
#        
#    Examples
#    --------
#    >>> td = datetime.timedelta(4.5)
#    >>> td
#    datetime.timedelta(4, 43200)
#    >>> timedelta_to_days(td)
#    4.5
#    
#    """
#    seconds_in_day = 24. * 3600.
#    
#    days = td.days + (td.seconds + (td.microseconds * 10.e6)) / seconds_in_day
#    
#    return days
    
    
class datetime(dt.datetime):
    """
    A subclass of `datetime.datetime` that performs math operations by first
    converting to Julian Day, then back to a `jdutil.datetime` object.
    
    Addition works with `datetime.timedelta` objects, subtraction works with
    `datetime.timedelta`, `datetime.datetime`, and `jdutil.datetime` objects.
    Not all combinations work in all directions, e.g.
    `timedelta - datetime` is meaningless.
    
    See Also
    --------
    datetime.datetime : Parent class.
    
    """
    def __add__(self,other):
        if not isinstance(other,dt.timedelta):
            s = "jdutil.datetime supports '+' only with datetime.timedelta"
            raise TypeError(s)
        
        days = timedelta_to_days(other)
        
        combined = datetime_to_jd(self) + days
        
        return jd_to_datetime(combined)
        
    def __radd__(self,other):
        if not isinstance(other,dt.timedelta):
            s = "jdutil.datetime supports '+' only with datetime.timedelta"
            raise TypeError(s)
        
        days = timedelta_to_days(other)
        
        combined = datetime_to_jd(self) + days
        
        return jd_to_datetime(combined)
        
    def __sub__(self,other):
        if isinstance(other,dt.timedelta):
            days = timedelta_to_days(other)
            
            combined = datetime_to_jd(self) - days
            
            return jd_to_datetime(combined)
            
        elif isinstance(other, (datetime,dt.datetime)):
            diff = datetime_to_jd(self) - datetime_to_jd(other)
            
            return dt.timedelta(diff)
            
        else:
            s = "jdutil.datetime supports '-' with: "
            s += "datetime.timedelta, jdutil.datetime and datetime.datetime"
            raise TypeError(s)
            
    def __rsub__(self,other):
        if not isinstance(other, (datetime,dt.datetime)):
            s = "jdutil.datetime supports '-' with: "
            s += "jdutil.datetime and datetime.datetime"
            raise TypeError(s)
            
        diff = datetime_to_jd(other) - datetime_to_jd(self)
            
        return dt.timedelta(diff)
        
    def to_jd(self):
        """
        Return the date converted to Julian Day.
        
        """
        return datetime_to_jd(self)
        
    def to_mjd(self):
        """
        Return the date converted to Modified Julian Day.
        
        """
        return jd_to_mjd(self.to_jd())


if False:
    try:
        import convtimeX as cv
    
        PreciseTime = cv.PreciseTime
        DeltaTime = cv.DeltaTime
        convtime = cv.convtime
        yyyy_to_yy = cv.yyyy_to_yy
        yy_to_yyyy = cv.yy_to_yyyy
    
    except:
        pass


def last_doy(yyyy):
    """Return day of year of December 31

    >>> last_doy(2016)
    366
    """

    _, ddd, _, _, _ = convtime("cal", "doy", [yyyy, 12, 31, 0, 0, 0])
    return ddd

def format_time(istr, pe):
    """Return string representation of time

    >>> pe = PreciseTime("cal", [2017, 1, 1, 0, 0, 0.000000000001])

    >>> format_time("[MJD3] [WWWW] [D] [DSEC6]", pe)
    '57754.000 1930 0 00000.000000'

    >>> format_time("[YYYY] [DDD] [MM] [DD] [HH] [MN] [SS12]", pe)
    '2017 001 01 01 00 00 00.000000000001'
    """

    def find_precision(istr, keyword):
        ind0 = istr.find("[%s"%(keyword))
        ind1 = ind0 + len(keyword) + 1
        ind2 = ind1 + istr[ind1:].find("]")
        prec = int(istr[ind1:ind2])

        return prec

    def format_float(istr, keyword, ulen, val):
        ind0 = istr.find("[%s"%(keyword))
        ind1 = ind0 + len(keyword) + 1
        ind2 = ind1 + istr[ind1:].find("]")
        prec = int(istr[ind1:ind2])
        if prec == 0:
            tlen = ulen
        else:
            tlen = ulen + 1 + prec
        fstr = "%%0%d.%df"%(tlen, prec)
        istr = istr.replace(istr[ind0:ind2+1], fstr%(val))

        return istr

    if isinstance(pe, PreciseTime):
        mjd2 = pe.get("mjd2")

    ### Find out sec precision first

    aprx = 99
    if istr.find("[SS") > -1:
        prec = find_precision(istr, "SS")
        aprx = 1/(10)**prec

    if istr.find("[DSEC") > -1:
        prec = find_precision(istr, "DSEC")
        aprx = 1/(10)**prec

    yyyy, mm, dd, hh, mn, ss = convtime("mjd2", "cal", mjd2, aprx)
    yyyy, ddd = convtime("mjd2", "doy", mjd2, aprx)[:2]
    gwkn, gwkd = convtime("mjd2", "gps2", mjd2, aprx)[:2]
    mjd = convtime("mjd2", "mjd", mjd2)
    dsec = hh*3600 + mn*60 + ss

    yy = yyyy_to_yy(yyyy)

    istr = istr.replace("[WWWW]", "%04d"%(gwkn))
    istr = istr.replace("[D]", "%d"%(gwkd))
    istr = istr.replace("[YYYY]", "%04d"%(yyyy))
    istr = istr.replace("[YY]", "%02d"%(yy))
    istr = istr.replace("[DDD]", "%03d"%(ddd))
    istr = istr.replace("[MM]", "%02d"%(mm))
    istr = istr.replace("[DD]", "%02d"%(dd))
    istr = istr.replace("[HH]", "%02d"%(hh))
    istr = istr.replace("[MN]", "%02d"%(mn))

    if istr.find("[MJD") > -1:
        istr = format_float(istr, "MJD", 5, mjd)

    if istr.find("[SS") > -1:
        istr = format_float(istr, "SS", 2, ss)

    if istr.find("[DSEC") > -1:
        istr = format_float(istr, "DSEC", 5, dsec)

    return istr

