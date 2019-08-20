#!/usr/bin/env python3

"""
Module with common geodetic transformations.

Product of: 
U.S. Nat.'l Geodetic Survey / Nat.'l Oceanic Atmospheric Admin.
1315 East-West Hwy.
Silver Spring, MD, 20910

Authors:
Sungpil Yoon
Phillip McFarland

Contact:
phillip.mcfarland@noaa.gov

As required by 17 U.S.C. § 403, third parties producing copyrighted works consisting predominantly 
of the material appearing in NGS Web pages must provide notice with such work(s) identifying the NGS 
material incorporated and stating that such material is not subject to copyright protection.
"""


import math as M
import numpy as np
import pytest


DEG_TO_RAD = M.pi/180
D2R = DEG_TO_RAD
R2D = 1/D2R

# define Earth ellipsoid parameters for WGS84:

a = 6378137.0                   # length of semi-major axis (m)
inv_f = 298.257223563           # reciprical flattening (unitless)

# Ref: Misra, P. & Enge, P. "Global Positioning System", 2nd ed., p. 103
#-----------------------------------------------------------------------

# compute derived quantities from WGS84 definitions above:

a2 = a*a                        # semi-major axis squared (m^2)
f = 1.0/inv_f                   # flattening (unitless)
e2 = 2.0*f - f*f                # eccentricity squared (unitless)
b2 = a2 - a2*e2                 # semi-minor axis squared (m^2)

# Ref: Misra, P. & Enge, P. "Global Positioning System", 2nd ed., p. 98
#-----------------------------------------------------------------------

def compute_F(h, phi, x, y, z):
    
    """Compute F the vector valued function that gives 
    the misfit between h and phi passed to the function and
    the true h and phi associated with the point given by (x,y,z). 
    F is defined as:
    
         | f(h, phi)|
     F = |          |     where:
         | g(h, phi)| 
    
            p                          (         z          ) 
     f = -------  - N - h ;  g = arctan( ------------------ ) - phi ;
         cos(phi)                      ( 1 - e^2*sin(phi)^2 ) 
    
   
                     a
     N = -------------------------- ;   and     p = (x^2 + y^2)^(1/2)
         (1 - e^2*sin(phi)^2)^(1/2)
    
    Ref: Misra, P. & Enge, P. "Global Positioning System", 2nd ed., p. 134 - 135
    """
    # compute necessary trig. functions w.r.t. phi
    sinPhi = np.sin(phi)
    sinPhi2 = sinPhi*sinPhi
    cosPhi = np.cos(phi)
    
    # compute N and p
    N = a/np.sqrt(1.0 - e2*sinPhi2)
    p = np.sqrt(x*x + y*y)

    # compute f and g
    f = p/cosPhi - N - h
    
    g_term1 = np.arctan(z/(p*(1.0 - e2*N/(N + h))))
    g = g_term1 - phi

    F = [f,g]
    
    return F

#-------------------------------------------------------------------------------

def compute_Jac_F(h, phi, x, y, z):

    """Compute the Jacobian of F (J_F) evaluated at h and phi where:
    
           | df     df  |
           | --    ---- |
           | dh    dphi |
     J_F = |            |
           | dg     dg  |
           | --    ---- |
           | dh    dphi |
    
    see function: compute_F for definitions of f and g
    """ 
    # compute necessary trig. functions for phi
    sinPhi = np.sin(phi)
    sinPhi2 = sinPhi*sinPhi
    cosPhi = np.cos(phi)
    cosPhi2 = cosPhi*cosPhi

    # compute N and p
    N = a/np.sqrt(1.0 - e2*sinPhi2)
    p = np.sqrt(x*x + y*y)
    p2 = p*p

    # define a few convenient intermediate terms

    q = p2*(h - e2*N + N)*(h - e2*N + N) + z*z*(h+N)*(h+N)
    s = N*e2*sinPhi*cosPhi/(1.0 - e2*sinPhi2)
    
    # compute the four partials

    dfdh = -1.0

    dfdphi = p*sinPhi/cosPhi2 - s

    dgdh = (-1.0)*e2*N*p*z/q

    dgdphi = (e2*h*p*z*s/q) - 1.0
    
    # built J_F for output
    J_F = [dfdh, dfdphi, dgdh, dgdphi]

    return J_F

#----------------------------------------------------------------------------

def xyz_to_llh(x, y, z):
    
    """Convert cartesian coordinates to WGS84 lat., lon., and height above
    reference ellipsoid. Cartesian coordinates must be passed in meters. 
    Latitude and longitude are returned in degrees and height is returned in
    meters. With:

        -90 < lat. < 90     and       0 < lon. < 360

    Routine starts with an initial guess assuming a spherical Earth and then
    iterates towards the WGS84 solution using Newton's method.

    Example:

    >>> x, y, z = 100000, 100000, 1000000
    >>> xyz_to_llh(x, y, z)
    [82.27427630552833, 45.0, -5347205.038887162]
    
    Ref: Misra, P. & Enge, P. "Global Positioning System", 2nd ed., p. 134-135
    """
    # convert inputs to floats
    x = float(x)
    y = float(y)
    z = float(z)

    # method fails when x and y are both exactly 0; exit and return
    # error message under this condition:

    if x == 0.0 and y == 0.0:
        exit("error:  x and y cannot both be exactly zero, point must be at least 1e-11 m from pole")
    
    # compute the longitude
    preLon = np.arctan2(y,x)    # arctan2 returns angle in rads 
                                # between [-pi, pi]

    radLon = preLon%(2*np.pi)   # modulo 2*pi returns value 
                                # in rads between [0, 2*pi)

    # compute the projection in the xy-plane of the line extending 
    # from the z-axis to the point that is  normal to the ellipsoid at
    # the surface

    p = np.sqrt(x*x + y*y)
    
    # Newton's method requires initial guess
    # start with guess assuming spherical Earth
    # with radius equal to Earth's semi-major axis

    radE0 = a 
    dist0 = np.sqrt(x*x + y*y + z*z)
    h_prime = dist0 - radE0
    lat_prime = np.arctan2(z,p)     # p is always positive, so even though arctan2
                                    # returns angle in [-pi,pi] with p positive
                                    # lat will always be in [-pi/2,pi/2]

    # compute misfit between actual and initial guess
    
    f_prime, g_prime = compute_F(h_prime, lat_prime, x, y, z)

    # while the error in h and phi is greater than 1e-9 meters
    # keep iterating toward a better solution (note: latitude error 
    # (i.e. g_prime) is still in radians at this point. And 1e-12 
    # radians of latitude is about 1e-9 meters)
    
    # add counter variable
    counter = 0
    while np.absolute(f_prime) > 1e-9 or np.absolute(g_prime) > 1e-12:
        
        # compute the next guess for h and lat

        # first get derivatives evaluated at last guess for h and lat

        dfdh, dfdlat, dgdh, dgdlat = compute_Jac_F( h_prime, lat_prime, x, y, z)

        # combine elements of the  Jacobian into numpy array

        jacobian = np.array([[dfdh, dfdlat],[dgdh, dgdlat]])
        
        # invert the jacobian

        inv_jac = np.linalg.inv(jacobian)

        # get the values for F from last guess for h and lat
        # see compute_F documentation for definition of F
        
        f_prime, g_prime = compute_F(h_prime, lat_prime, x, y, z)

        # combine elements of F into numpy array
        
        F = np.array([f_prime, g_prime])

        # make vector of h_prime and lat_prime

        v_prime = np.array([h_prime, lat_prime])

        # compute next guess for v using Newton's method

        v_new = v_prime.T - np.matmul(inv_jac,F.T)

        # update values for h_prime and lat_prime

        h_prime = v_new[0]
        lat_prime = v_new[1]

        counter = counter + 1

        if counter > 2000
            break
            print(f'ERROR: loop hit {counter} iterations before meeting convergence criteria')
            return -1
    
    # h is last guess h_prime
    # radLat is last guess lat_prime in radians
    h = h_prime
    radLat = lat_prime
    
    # build llh for output and convert lat and long to deg
    llh = [R2D*radLat, R2D*radLon, h]
    
    return llh

#-----------------------------------------------------------------------

def test_xyz_to_llh():
    
    """unit test for xyz_to_llh

    test creates three random 1x10000 arrays for lon, lat and height:

        lon: 0 < lon < 2*pi
        lat: -pi/2 < lat < pi/2
        height: -3000 m < h < 3000 m

    these arrays are combined element-wise to form coordinate triplets
    (i.e. [lat[0], lon[0], h[0]] is the first coordinate triplet formed)
    Each coordinate triplet is converted to cartesian coordinates using
    llh_to_xyz. The returned cartesian coordinates are then converted to
    lat, lon, and ht using xyz_to_llh and the results are comapred to 
    the original randomly generated coordinates. The test is passed if
    the final returned geodetic coordinates are the same as the 
    randomly generated geodetic coordinates within the designated
    tolerance. The tolerance should be at least 2 orders of magnitude
    smaller than the desired precision. (i.e. if mm level precision is 
    required then the tolerance should be set to 1e-5 for ht and 1e-10
    for latitude and longitude)
    """
    lonInitArray = np.pi*2*np.random.rand(1, 10000)
    latInitArray = (np.pi/2)*(np.random.rand(1, 10000) - 0.5)
    hInitArray = 3000.0*np.random.rand(1, 10000)
    
    for i, lon in enumerate(lonInitArray[0,:]):
        
        lat = latInitArray[0,i]
        h = hInitArray[0,i]

        lon = lon*R2D
        lat = lat*R2D
        
        x, y, z = llh_to_xyz( lat, lon, h)

        latOut, lonOut, hOut =  xyz_to_llh( x, y, z)

        assert latOut == pytest.approx(lat, abs=1e-13) # 2 orders of mag smaller than mm
        assert lonOut == pytest.approx(lon, abs=1e-13) # 2 orders of mag smaller than mm
        assert hOut == pytest.approx(h, abs=1e-8) # 5 orders of mag smaller than mm

#-----------------------------------------------------------------------

def llh_to_xyz( lat, lon, h):

    """
    Takes latitude, longitude and height above reference ellipsoid and
    returns cartesian coordinates. Latitude must be in degrees between
    -90 and 90, longitude must be in degrees between 0 and 360 and height
    must be in meters. Transformation assumes lat, lon and height are 
    given with respect to WGS84.

    xyz are returned in meters
    
    Ref: Misra, P. & Enge, P. "Global Positioning System", 2nd ed., p. 134
    """
    latRad = D2R*lat
    lonRad = D2R*lon
    
    sinLon = np.sin(lonRad)
    cosLon = np.cos(lonRad)
    sinLon2 = sinLon*sinLon
    cosLon2 = cosLon*cosLon

    sinLat = np.sin(latRad)
    cosLat = np.cos(latRad)
    sinLat2 = sinLat*sinLat
    cosLat2 = cosLat*cosLat

    N = a/np.sqrt(1.0 - e2*sinLat2)

    x = (N + h)*cosLat*cosLon
    y = (N + h)*cosLat*sinLon
    z = (N*(1.0 - e2) + h)*sinLat

    xyz = [x,y,z]

    return xyz

#-----------------------------------------------------------------------


def xyz_to_neu(lat, lon, x, y, z):
    """Convert geocentric x, y, z vector to local north, east, up

    @param lat
    @param lon
    @param x
    @param y
    @param z

    @return n
    @return e
    @return u
    """

    clat= M.cos( lat*DEG_TO_RAD );
    slat= M.sin( lat*DEG_TO_RAD );
    clon= M.cos( lon*DEG_TO_RAD );
    slon= M.sin( lon*DEG_TO_RAD );
    
    e= -x*slon + y*clon;
    n= -x*slat*clon - y*slat*slon + z*clat;
    u= +x*clat*clon + y*clat*slon + z*slat;

    return n, e, u

def xyz_to_enu(lat, lon, x, y, z):
    n, e, u = xyz_to_neu(lat, lon, x, y, z)

    return e, n, u

def xyz_to_enu_cov(lat, lon, covmat):
    clat= M.cos( lat*DEG_TO_RAD )
    slat= M.sin( lat*DEG_TO_RAD )
    clon= M.cos( lon*DEG_TO_RAD )
    slon= M.sin( lon*DEG_TO_RAD )

    R = np.array([[-slon, clon, 0],
                [-slat*clon, -slat*slon, clat],
                [clat*clon, clat*slon, slat]])

    new_mat = R.dot(covmat.dot(R.T))

    return new_mat


def xyz_to_llh_est(x, y, z, a=6378137, e=8.1819190842622e-2):
    """

    Reference:

    https://www.mathworks.com/matlabcentral/fileexchange/7941-convert-cartesian--ecef--coordinates-to-lat--lon--alt?s_tid=gn_loc_drop

    Examples:

    >>> x, y, z = 100000, 100000, 1000000
    >>> xyz_to_llh(x, y, z)
    (82.27428701521953, 45.0, -5347203.590487044)

    >>> x, y, z = 100000, 1000000, 1000000
    >>> xyz_to_llh(x, y, z)
    (45.72167099095937, 84.28940686250037, -4949596.361699604)
    """

    a2 = a*a
    e2 = e*e

    b = M.sqrt(a2*(1 - e2))
    b2 = b*b

    ep = M.sqrt((a2 - b2)/b2)
    p = M.sqrt(x**2 + y**2)
    th = M.atan2(a*z, b*p)
    lon = M.atan2(y, x)
    lat = M.atan2(z + ep**2*b*M.sin(th)**3, p - e2*a*M.cos(th)**3)
    N = a/M.sqrt(1 - e2*M.sin(lat)**2)
    alt = p/M.cos(lat) - N

    # Return lon in range(0, 2*pi)
    lon = lon%(2*M.pi)

    # correct for numerical instability in altitude near exact poles:
    # (after this correction, error is about 2 millimeters, which is about
    # he same as the numerical precision of the overall function)

    if abs(x) < 1 and abs(y) < 1:
        alt = abs(z) - b

    return lat*R2D, lon*R2D, alt


def normalize(vec):
    vec = np.array(vec)
    norm = np.linalg.norm(vec)
    return vec/norm

def compute_rotmat_to_body(pos, vel):
    """body_x -- velocity (along-track) direction
    body_y -- cross-track
    body-z -- radial direction
    """

    pos = np.array(pos)
    vel = np.array(vel)

    xi = normalize(vel)
    yi = normalize(np.cross(pos, vel))
    zi = normalize(np.cross(xi, yi))
    mat = np.array([xi, yi, zi])

    return mat

def rotate(mat, vec):
    return mat.dot(np.array(vec).reshape((3, 1))).flatten().tolist()


