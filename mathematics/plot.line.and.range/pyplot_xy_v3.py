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


def get_root(input_array, group1_index, group2_index):
    """
    :param input_array: T.B.D
    :param group1_index:  valid input should be 0 or 1
    :param group2_index:  valid input should be 0 or 1
    :return: T.B.D
    """
    if group1_index == 1:
        group1_index = 3

    if group2_index == 1:
        group2_index = 3

    a = np.array([input_array[0][1:3], input_array[1][1:3]])
    b = np.array([input_array[0, group1_index], input_array[1, group2_index]])
    x = np.linalg.solve(a, b)
    return x


def get_min_and_max_for_target(input_array, target_array):
    input_for_solve = np.array([[input_array[0][1], input_array[1][1]], [input_array[0][2], input_array[1][2]]])
    target_root = np.linalg.solve(input_for_solve, target_array)
    # print(target_root)

    min1 = input_array[0][0]
    max1 = input_array[0][3]
    min2 = input_array[1][0]
    max2 = input_array[1][3]
    if target_array[0] < 0:
        min1, max1 = max1, min1
    if target_array[1] < 0:
        min1, max1 = max1, min1

    result_min = 1.0 * target_root[0] * min1 + 1.0 * target_root[1] * min2
    result_max = 1.0 * target_root[0] * max1 + 1.0 * target_root[1] * max2
    if result_min > result_max:
        result_min, result_max = result_max, result_min
    return result_min, result_max


def solve_and_visualize_result(input_array, target_array):
    ax = plt.subplot()
    move_axis_to_middle(ax)

    x = np.arange(-10.0, 10.0, 0.01)

    # Line for: x + y < 3
    function1 = 1.0 * np.subtract(input_array[0][3], x * input_array[0][1]) / input_array[0][2]  # 3
    # Line for: "x + y > -2"
    function2 = 1.0 * np.subtract(input_array[0][0], x * input_array[0][1]) / input_array[0][2]  # -2

    # Line for: "x - y > -1"
    function3 = 1.0 * np.subtract(input_array[1][3], x * input_array[1][1]) / input_array[1][2]  # 1
    # Line for: "x - y < 4"
    function4 = 1.0 * np.subtract(input_array[1][0], x * input_array[1][1]) / input_array[1][2]  # 4

    line1, = plt.plot(x, function1, lw=2, label="x + y = 4")
    line2, = plt.plot(x, function2, lw=2, label="x + y = -2")
    line3, = plt.plot(x, function3, lw=2, label="x - y = -1")
    line4, = plt.plot(x, function4, lw=2, label="x - y = 4")

    root_1 = tuple(get_root(input_array, 0, 0))
    root_2 = tuple(get_root(input_array, 0, 1))
    root_3 = tuple(get_root(input_array, 1, 1))
    root_4 = tuple(get_root(input_array, 1, 0))

    # Make the shaded region. Below URL is the guide.
    # https://matplotlib.org/gallery/showcase/integral.html#sphx-glr-gallery-showcase-integral-py
    # verts = [(-0.5, -1.5)] +  [(2, 1)] +  [(3.5, -0.5)] +  [(1, -3)]
    verts = [root_1, root_2, root_3, root_4]
    # poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    poly = Polygon(verts, color='yellow')
    ax.add_patch(poly)

    # Show label. Below URL is the guide.
    # https://stackoverflow.com/questions/17941083/how-to-label-a-line-in-matplotlib-python/17942066
    plt.legend()
    plt.ylim(-10, 10)
    ax = plt.gca()

    result_min, result_max = get_min_and_max_for_target(input_array, target_array)
    output = str(result_min) + " < " + str(target_array[0]) + "x + " + str(target_array[1]) + "y < " + str(result_max)
    # https: // matplotlib.org / users / text_intro.html
    ax.text(1, 9, output, style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    plt.show()


if __name__ == '__main__':
    # If ..... -2 < x + y < 3, and 1 < x - y < 4
    input_array = np.array([[-2, 1, 1, 3], [1, 1, -1, 4]])

    # Our target: What is the range of z = 2x - 3y ?
    target_array = np.array([2, -3])

    # Solve this problem and visualize the result.
    solve_and_visualize_result(input_array, target_array)
