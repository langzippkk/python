# MPCS 51042-1 2018: Ray Tracing Challenge

## Intro

The file `ray_tracer_solution.py` contains two implementations of a ray tracer:
* `TracerBasic`: Contains a non-vectorized version.  It relies on a four loop
   for everything except for some very short (length 3) dot products.
*  `TracerOpt`:  Contains a vectorized version.  Everything is vectorized
   except for updating the image.  I couldn't figure that out!
   
## Usage

`ray_tracer_solution.py` can be run as an executable with the following options:
* `-m`, `--mode`:  Run in optimized or basic mode. Choices: 'opt', 'basic' (default: 'opt')
* `-n`, `--nrays`: Number of view rays to simulate (default: 1000)
* `-g`, `--grid_size`: Size of image grid in pixels (default: 100]
* `-c`, `--cmap`: A matplotlib colormap for the image (default: 'copper')
