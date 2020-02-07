#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import argparse
import time


class RayTraceErr(Exception):
    pass


def rand_angle():
    return np.pi * np.random.random()


def get_view_ray():
    theta, phi = rand_angle(), rand_angle()
    return np.array([np.sin(theta) * np.cos(phi),
                     np.sin(theta) * np.sin(phi),
                     np.cos(theta)])


def get_isect_window(view_ray, window_loc, window_max):
    isect = window_loc / V[1] * view_ray
    if np.abs(isect[0]) > window_max or np.abs(isect[2]) > window_max:
        raise RayTraceErr
    else:
        return isect


def get_isect_sphere(view_ray, center_sphere, radius_sphere):
    v_dot_c = view_ray.dot(center_sphere)
    c_dot_c = center_sphere.dot(center_sphere)

    root_operand = v_dot_c ** 2 + radius_sphere ** 2 - c_dot_c
    if root_operand < 0:
        raise RayTraceErr
    else:
        t = v_dot_c - np.sqrt(root_operand)
        return t * view_ray


def get_brightness(isect_sphere, center_sphere, light_loc):
    i_minus_c = isect_sphere - center_sphere
    norm_sphere = i_minus_c / np.linalg.norm(i_minus_c)

    l_minus_i = light_loc - isect_sphere
    source_dir = l_minus_i / np.linalg.norm(l_minus_i)

    s_dot_n = source_dir.dot(norm_sphere)

    return max(0, s_dot_n)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nrays", type=int, default=1000, help="Number of view rays to simulate [default: 1000]")
    parser.add_argument("-g", "--ngrid", type=int, default=100, help="Edge length of image grid in pixels [default: 1000]")
    parser.add_argument("-c", "--cmap", default="copper", help="A matplotlib colormap [default: 'copper']")
    parser.add_argument("-o", "--output", default="sphere.png", help="Name of output image [default: 'sphere.png']")
    args = parser.parse_args()

    grid = np.zeros(shape=(args.ngrid, args.ngrid))
    window_max = 10
    window_loc = 10
    center_sphere = np.array([0, 12, 0])
    radius_sphere = 6
    light_loc = np.array([4, 4, -1])

    coord_to_idx = lambda coord: np.rint(coord / (2 * window_max / (args.ngrid - 1)) + (args.ngrid - 1) / 2)

    i = 0
    telapsed = 0
    while i < args.nrays:
        try:
            tstart = time.time()
            V = get_view_ray()
            W = get_isect_window(view_ray=V, window_loc=window_loc, window_max=window_max)
            I = get_isect_sphere(view_ray=V, center_sphere=center_sphere, radius_sphere=radius_sphere)
            b = get_brightness(isect_sphere=I, center_sphere=center_sphere, light_loc=light_loc)
            x = int(coord_to_idx(W[0]))
            z = int(coord_to_idx(W[2]))
            grid[x][z] += b
            i += 1
            tend = time.time()
        except RayTraceErr:
            continue
        else:
            telapsed += (tend - tstart)
            if i % 1000 == 0:
                print('\r{:.1%} finished ... '.format(i/args.nrays), end='')
    print('done!')

    print('Total elapsed time: {:g} s'.format(telapsed))
    print('Avg time per ray: {:g} s'.format(telapsed / args.nrays))

    plt.imshow(grid, cmap=args.cmap)
    plt.savefig(args.output)
    plt.show()


