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

def get_root(input_info, group1_index, group2_index):
    """
    :param input_info: T.B.D
    :param group1_index:  valid input should be 0 or 1
    :param group2_index:  valid input should be 0 or 1
    :return: T.B.D
    """
    if group1_index == 1:
        group1_index = 3

    if group2_index == 1:
        group2_index = 3

    a = np.array([input_info[0][1:3], input_info[1][1:3]])
    b = np.array([input_info[0, group1_index], input_info[1, group2_index]])
    x = np.linalg.solve(a, b)
    return x

if __name__ == '__main__':
    """
    Now every we need to do is just changing the input. And then everything will be calculated based on it.  
    """
    # If ..... -2 < x + y < 3, and 1 < x - y < 4
    input = np.array([[-2, 1, 1, 3], [1, 1, -1, 4]])

    ax = plt.subplot()
    move_axis_to_middle(ax)

    x = np.arange(-10.0, 10.0, 0.01)

    # Line for: x + y < 3
    function1 = 1.0 * np.subtract(input[0][3], x * input[0][1]) / input[0][2]  # 3
    # Line for: "x + y > -2"
    function2 = 1.0 * np.subtract(input[0][0], x * input[0][1]) / input[0][2] # -2

    # Line for: "x - y > -1"
    function3 = 1.0 * np.subtract(input[1][3], x * input[1][1]) / input[1][2]  # 1
    # Line for: "x - y < 4"
    function4 = 1.0 * np.subtract(input[1][0], x * input[1][1]) / input[1][2]  # 4

    line1, = plt.plot(x, function1, lw=2, label ="x + y = 4")
    line2, = plt.plot(x, function2, lw=2, label ="x + y = -2")
    line3, = plt.plot(x, function3, lw=2, label ="x - y = -1")
    line4, = plt.plot(x, function4, lw=2, label ="x - y = 4")

    root_1 = tuple(get_root(input, 0, 0))
    root_2 = tuple(get_root(input, 0, 1))
    root_3 = tuple(get_root(input, 1, 1))
    root_4 = tuple(get_root(input, 1, 0))

    # Make the shaded region. Below URL is the guide.
    # https://matplotlib.org/gallery/showcase/integral.html#sphx-glr-gallery-showcase-integral-py
    # verts = [(-0.5, -1.5)] +  [(2, 1)] +  [(3.5, -0.5)] +  [(1, -3)]
    verts = [root_1 , root_2, root_3, root_4]
    # poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    poly = Polygon(verts, color='yellow')
    ax.add_patch(poly)

    # Show label. Below URL is the guide.
    # https://stackoverflow.com/questions/17941083/how-to-label-a-line-in-matplotlib-python/17942066
    plt.legend()
    plt.ylim(-10,10)
    ax=plt.gca()

    plt.show()
