import cmath as c
import design_helpers as dh

def get_line_coeffs(z1, z2):
    return c.polar(z2 - z1)


    pass

def get_intersect_from_zs(pair1, pair2):
    """ Find the intersect of 2 lines given 2 pairs of complex points.

    Checks to see if an intersect exists between lines drawn from point1
    through point2 in each line. Note that this is deliberately directional,
    Will not fin an intercept drawn from point2 through point 1.

    Returns the complex number correspondint to the intercept or None
    """
    p1, p2 = pair1
    p3, p4 = pair2
    t = abs((p3 - p1) / (p2 + p3 - p1 - p4))
    if (p1 + (p2 - p1)*t) == p3 + (p4 - p3)*t:
        return p1 + (p2 - p1)*t
    return None

z1 = complex(0,0)
z2 = complex(0.5,1)
z3 = complex(3,0)
z4 = complex(2.5,1)

intersect = get_intersect_from_zs((z1, z2), (z3, z4))
print(intersect)
