#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import argparse
import time
import warnings
from abc import ABC, abstractmethod


class RayTraceErr(Exception):
    pass


class TracerABC(ABC):
    def __init__(self, grid_size, window_size, window_loc, sphere_loc, sphere_radius, light_loc):
        self._grid_size = grid_size
        self._window_size = window_size
        self._window_loc = window_loc
        self._sphere_loc = sphere_loc
        self._sphere_radius = sphere_radius
        self._light_loc = light_loc

        self._ntotal_rays = 0

        self.window = np.zeros((self._grid_size, self._grid_size))

    @abstractmethod
    def simulate_rays(self, nrays):
        raise NotImplemented

    def update_window(self, window_intersect, brightness):
        # idx are the indices in `window` that correspond to each view ray's coordinates.
        # idx.shape = (3, n)
        idx = np.rint(window_intersect
                      / (2 * self._window_size / (self._grid_size - 1))
                      + (self._grid_size - 1) / 2).astype(int)

        # Finally add the brightness to each gridpoint in window
        # To make the for loop work, We have to transpose idx.  It might be
        # possible to do a clever vectorized collective
        for bval, coord in zip(brightness, idx.T):
            self.window[coord[0], coord[2]] += bval


class TracerBasic(TracerABC):

    def __init__(self, grid_size, window_size, window_loc, sphere_loc, sphere_radius, light_loc):

        TracerABC.__init__(self, grid_size=grid_size, window_size=window_size, window_loc=window_loc,
                           sphere_loc=sphere_loc, sphere_radius=sphere_radius, light_loc=light_loc)

        self._sphere_loc.shape = (3,)
        self._light_loc.shape = (3,)

    def get_view_ray(self):
        view_angle = np.arctan(self._window_size / self._window_loc)
        a, b = view_angle, np.pi - view_angle

        theta = (b - a) * np.random.random_sample() + a
        phi = (b - a) * np.random.random_sample() + a

        return np.array([np.sin(theta) * np.cos(phi),
                         np.sin(theta) * np.sin(phi),
                         np.cos(theta)])

    def get_isect_window(self, view_ray):
        isect = self._window_loc / view_ray[1] * view_ray
        if np.abs(isect[0]) > self._window_size or np.abs(isect[2]) > self._window_size:
            raise RayTraceErr
        else:
            return isect

    def get_isect_sphere(self, view_ray):
        v_dot_c = view_ray.dot(self._sphere_loc)
        c_dot_c = self._sphere_loc.dot(self._sphere_loc)

        root_operand = v_dot_c ** 2 + self._sphere_radius ** 2 - c_dot_c
        if root_operand < 0:
            raise RayTraceErr
        else:
            t = v_dot_c - np.sqrt(root_operand)
            return t * view_ray

    def get_brightness(self, isect_sphere):
        i_minus_c = isect_sphere - self._sphere_loc
        norm_sphere = i_minus_c / np.linalg.norm(i_minus_c)

        l_minus_i = self._light_loc - isect_sphere
        source_dir = l_minus_i / np.linalg.norm(l_minus_i)

        s_dot_n = source_dir.dot(norm_sphere)

        return max(0, s_dot_n)

    def coord_to_idx(self, coord):
        return np.int(np.rint(coord / (2 * self._window_size / (self._grid_size - 1)) + (self._grid_size - 1) / 2))

    def simulate_rays(self, nrays):
        i = 0
        while i < args.nrays:
            try:
                # print('\r{:.1%} finished ... '.format(i / args.nrays), end='')
                V = self.get_view_ray()
                W = self.get_isect_window(view_ray=V)
                I = self.get_isect_sphere(view_ray=V)
                b = self.get_brightness(isect_sphere=I)
                x = int(self.coord_to_idx(W[0]))
                z = int(self.coord_to_idx(W[2]))
                self.window[x, z] += b
                i += 1
            except RayTraceErr:
                continue
        # print('done!')
        return nrays


class TracerOpt(TracerABC):

    def __init__(self, grid_size, window_size, window_loc, sphere_loc, sphere_radius, light_loc):
        TracerABC.__init__(self, grid_size=grid_size, window_size=window_size, window_loc=window_loc,
                           sphere_loc=sphere_loc, sphere_radius=sphere_radius, light_loc=light_loc)

        self._sphere_loc.shape = (3, 1)
        self._light_loc.shape = (3, 1)

    def simulate_rays(self, nrays):
        C = self._sphere_loc
        W_y = self._window_loc
        W_max = self._window_size
        L = self._light_loc

        # =====================================================
        # 1. Get view rays, V
        # =====================================================

        # Get n random rays that reach the observer through the window
        view_angle = np.arctan(W_max / W_y)
        a, b = view_angle, np.pi - view_angle
        theta = (b - a) * np.random.random_sample((nrays,)) + a
        phi = (b - a) * np.random.random_sample((nrays,)) + a

        # V are the vector components of view rays:
        #   [[x1, x2, ..., xn],
        #    [y1, y2, ..., yn],
        #    [z1, z2, ..., zn]]
        V = np.empty((3, nrays))
        V[0, :] = np.sin(theta) * np.cos(phi)
        V[1, :] = np.sin(theta) * np.sin(phi)
        V[2, :] = np.cos(theta)

        # =====================================================
        # 2. Get the intersections of view rays with window
        # =====================================================

        # W are the coordinates where each view ray intersects the window:
        # The y coordinate will not be used when we plot the window.
        #   [[x1, x2, ..., xn],
        #    [y1, y2, ..., yn],
        #    [z1, z2, ..., zn]]
        W = W_y * V / V[1, :]

        # =====================================================
        # 3. Get the intersections of view rays with sphere
        # =====================================================

        # Intermediate values to get I
        # v_dot_c.shape == (n,)
        v_dot_c = np.sum(V * C, axis=0)
        # c_dot_c is scalar
        c_dot_c = np.sum(C * C, axis=0)
        # t.shape == (n,)
        t = v_dot_c - np.sqrt(v_dot_c ** 2 + self._sphere_radius ** 2 - c_dot_c)

        # I are the coordinates where each view ray intersects the sphere.
        #   [[x1, x2, ..., xn],
        #    [y1, y2, ..., yn],
        #    [z1, z2, ..., zn]]
        #
        # **NOTE THAT SOME OF THESE COORDINATES WILL BE NaN**, since
        # some view rays do not intersect the sphere and hence
        # will not have a real solution to our equation.
        #
        # We will ignore the NaNs (and associated runtime warning) for now.
        # At the end, we will make a mask for only the valid coords.
        I = t * V

        # =====================================================
        # 4. Get an observed brightness for each view ray
        # =====================================================

        # Intermediate value to get N
        # I_min_C.shape = (3, n)
        I_min_C = I - C

        # N are the vectors that are perpindicular to the sphere at each
        # view ray's intersection.  Again, some maybe NaN.
        # N.shape = (3, n)
        N = I_min_C / np.sqrt(np.sum(I_min_C * I_min_C, axis=0))

        # Intermediate values to get S
        # L_min_I.shape = (3, n)
        L_min_I = L - I

        # S is the vector pointing from the light source to each view
        # ray's intersection.  Again, there will be NaNs.
        # S.shape = (3, n)
        S = L_min_I / np.sqrt(np.sum(L_min_I * L_min_I, axis=0))

        # b is the observed brightness of each view ray.
        # [b1, b2, ..., bn].  Again, there will be NaNs.
        b = np.sum(S * N, axis=0)
        b[b < 0.] = 0.

        # =====================================================
        # 5. Get the mask for valid view rays.
        # =====================================================

        # Valid view rays are those that actually intersect with the
        # sphere.  This was determined when calculating I (part 3)
        # We can use the term t to tell if the solution to I was real.
        valid_mask = ~np.isnan(t) & ~np.isnan(b)
        valid_b = b[valid_mask]
        valid_W = W[:, valid_mask]

        # =====================================================
        # 6. Update the image
        # =====================================================

        self.update_window(window_intersect=valid_W, brightness=valid_b)

        # =====================================================
        # 6. Return num of valid view rays
        # =====================================================

        n_valid_rays = np.sum(valid_mask)
        self._ntotal_rays += n_valid_rays
        return n_valid_rays


if __name__ == '__main__':
    warnings.filterwarnings('ignore', category=RuntimeWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", default="opt", choices=["opt", "basic"],
                        help="Run optimized or basic mode [default: 'opt']")
    parser.add_argument("-n", "--nrays", type=int, default=100, help="Number of view rays to simulate [default: 1000]")
    parser.add_argument("-g", "--grid_size", type=int, default=100,
                        help="Length of image grid in pixels [default: 100]")
    parser.add_argument("-c", "--cmap", default="copper", help="A matplotlib colormap [default: 'copper']")
    args = parser.parse_args()

    window_size = 10
    window_loc = 10
    sphere_loc = np.array([0, 12, 0])
    sphere_radius = 6
    light_loc = np.array([4, 4, -1])

    if args.mode == "opt":
        tracer_obj = TracerOpt
    elif args.mode == "basic":
        tracer_obj = TracerBasic
    # This isn't strictly necessary, since we gave a "choice" parameter to parser.add_argument() above.
    else:
        raise argparse.ArgumentError("Provided invalid argument for '-m' or '--mode' (choices: 'opt', 'mode')")
    print("Run mode: " + args.mode)

    t = tracer_obj(grid_size=args.grid_size, window_size=window_size, window_loc=window_loc, sphere_loc=sphere_loc,
                   sphere_radius=sphere_radius, light_loc=light_loc)

    tstart = time.process_time()
    actual_nrays = t.simulate_rays(nrays=args.nrays)
    tend = time.process_time()
    telapsed = tend - tstart

    print('Total elapsed time: {:g} s'.format(telapsed))
    print('Avg time per ray: {:g} s\n'.format(telapsed / args.nrays))
    print('Fraction of valid rays: {:g} s'.format(actual_nrays / args.nrays))
    print('Avg time per valid ray: {:g} s'.format(telapsed / actual_nrays))

    plt.imshow(t.window, cmap=args.cmap)
    plt.show()
