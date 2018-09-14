# The purpose of this program

This python script is for my niece, because she discussed the following mathematics question with me. 
> If -2 < x + y < 3, and 1 < x - y < 4, 
> then what is the range of "z = 2x - 3y" ?

The correct answer is as below. And [answer.jpg](https://github.com/wang-qs/ForChildren/raw/master/mathematics/plot.line.and.range/answer.jpg) contains the approach to solution.
> 1 < z < 11

The question from my niece is that, 
>based on the above condition, the minimum value of x is -0.5, and the maximum value of y is 1, 
>then why the minimum of "z = 2x - 3y" is not -5 ?

The reason is that, 
> Although the mix of x is -0.5, and the max of y is 1, but x and y could not be their min value at the same time.
> For example, if they are the min value at the same time, then the condition "1 < x - y < 4" will be false.

To better understand the restrictions and the possible values of x and y. It is better to show my niece by picture. So I draw the following picture firstly. 

![manual_picture_to_show_x.y_range.jpg](https://github.com/wang-qs/ForChildren/raw/master/mathematics/plot.line.and.range/manual_picture_to_show_x.y_range.jpg)

But to make my niece and my children to be interesting in computer and programming, why not visulize it by program?  This is why I creted this python script, and the following picture is the final output.

<img src="https://github.com/wang-qs/ForChildren/raw/master/mathematics/plot.line.and.range/py_plot_output_to_show_x.y_range.jpg" width="588" height="642" title="py_plot_output_to_show_x.y_range.jpg">

# The 1st version

pyplot_xy.py is the 1st version. And the quadrangle in yellow is highlighted by the following hard code.

> verts = [(-0.5, -1.5)] +  [(2, 1)] +  [(3.5, -0.5)] +  [(1, -3)]

# The 2nd version

To move one more step, whether we could highlight the  quadrangle automatically? ( The point is to calculate the crossing point of the 4 lines automatically, and then we will know the range to highlight. )

This is the idea of the 2nd version, and it is implemented by pyplot_xy_v2.py

> a = np.array([input_info[0][1:3], input_info[1][1:3]]) <br />
> b = np.array([input_info[0, group1_index], input_info[1, group2_index]])<br />
> x = np.linalg.solve(a, b)<br />

And now, if the question changes, we only need to change the following "input" in the code, and then everything will be calculated automatically.

> \# If ..... -2 < x + y < 3, and 1 < x - y < 4 <br />
> input = np.array([[-2, 1, 1, 3], [1, 1, -1, 4]])

# The 3rd version

At last, whether we could ask computer to tell us the answer directly ( the range of "z = 2x - 3y") ? This is what the 3rd version does. It will move one more step and show the final answer directly as the following picture.

![final_output.jpg](https://github.com/wang-qs/ForChildren/raw/master/mathematics/plot.line.and.range/final_output.jpg)
