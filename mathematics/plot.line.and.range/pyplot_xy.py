import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def move_axis_to_middle(ax):
    # Drawing axis in the middle of the figure. Below URL is the guide.
    # https://stackoverflow.com/questions/31556446/drawing-axis-in-the-middle-of-the-figue-in-python

    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

if __name__ == '__main__':
    ax = plt.subplot()
    move_axis_to_middle(ax)

    x = np.arange(-10.0, 10.0, 0.01)

    # Line for: x + y < 4
    function1 = np.subtract(3, x)
    # Line for: "x + y > -2"
    function2 = np.subtract(-2, x)

    # Line for: "x - y > -1"
    function3 = np.add(-1, x)
    # Line for: "x - y < 4"
    function4= np.add(-4, x)

    line1, = plt.plot(x, function1, lw=2, label ="x + y = 4")
    line2, = plt.plot(x, function2, lw=2, label ="x + y = -2")
    line3, = plt.plot(x, function3, lw=2, label ="x - y = -1")
    line4, = plt.plot(x, function4, lw=2, label ="x - y = 4")


    # Make the shaded region. Below URL is the guide.
    # https://matplotlib.org/gallery/showcase/integral.html#sphx-glr-gallery-showcase-integral-py
    verts = [(-0.5, -1.5)] +  [(2, 1)] +  [(3.5, -0.5)] +  [(1, -3)]
    # poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    poly = Polygon(verts, color='yellow')
    ax.add_patch(poly)

    # Show label. Below URL is the guide.
    # https://stackoverflow.com/questions/17941083/how-to-label-a-line-in-matplotlib-python/17942066
    plt.legend()
    plt.ylim(-10,10)
    ax=plt.gca()

    plt.show()
