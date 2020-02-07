import numpy as np
import math
import matplotlib.pyplot as plt



def mandelbrot(step_size = 0.01,max_iterations = 1000):
	## When updating the mask, we need to use the for loop, because
	## we will need to calculate the result based on the current time and then
	## update it for future use. We can only do it in while or for loop.
    x1, y1 = np.meshgrid(np.arange(-2.0, 1.01, step_size,dtype=float), np.arange(-1.0, 1.01, step_size,dtype=float))
    x_len = len(np.arange(-2.0, 1.01, step_size,dtype=float))
    y_len = len(np.arange(-1.0, 1.01, step_size,dtype=float))
    a = complex(0,1)
    c = (y1*a+x1)
    c = c.flatten()
    z = np.zeros(shape=c.shape,dtype = complex)
    counter = np.zeros(shape=c.shape)
    mask = (abs(z) < 4) & (counter < max_iterations)
    while np.any(mask):
        z[mask] = z[mask]**2+c[mask]
    # update counter
        counter[mask] = counter[mask] + 1
    # update mask
        mask = np.where((abs(z)<4)&(counter< max_iterations))
    return (counter.reshape(y_len,x_len))

if __name__== "__main__":
    result = (mandelbrot(step_size = 0.01,max_iterations = 1000))
    plt.imshow(result)
    plt.show()