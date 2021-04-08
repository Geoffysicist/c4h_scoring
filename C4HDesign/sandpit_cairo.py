# from numpy.random._generator import default_rng
# from seaborn import color_palette
# from timeit import timeit
# from typing import List, Sequence
# import numpy as np
import cmath as c


def b_curve(control_points, n):
    return [
        b_point(control_points, id / (n-1))
        for id in range(n)
    ]


def b_point(control_points, t):
    # while len(control_points) > 1:
        # control_linestring = zip(control_points[:-1], control_points[1:])
        # control_linestring = control_points
        # for c in control_linestring: print(c)
    p1, p2, p3, p4 = control_points
    return p1*(1-t)**3 + 3*p2*(1-t)**2*(t)+3*p3*(1-t)*t**2+p4*t**3
    



def test():
    # degree 2, i.e. cubic Bézier with three control points per curve)
    # for large outputs (large number_of_curve_points)

    # controls = np.random.default_rng().random((3, 2), dtype=np.float64)
    controls = [complex(0,0), complex(0,1), complex(1,1), complex(1,0)]
    # controls = [(0.05911693, 0.51662047), (0.9908451, 0.28962062), [0.79028483, 0.91712453]]
    n_points = 8

    print(controls)

    curve = b_curve(controls, n_points)

    print(curve)


if __name__ == '__main__':
    test()