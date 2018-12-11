import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk

def point_on_line_check(la, lb, p):
    if np.array_equal(la, lb):
        print('There is no line. Two end points are the same!')
        return False

    ap = p - la # vector a -> p
    bp = p - lb # vector b -> p
    flag0 = np.linalg.norm(np.cross(ap, bp))
    flag = 0 # indication
    if flag0 == 0:
        info = 'The point is on the line AB.\n'
        # point on line AB

        if np.dot(ap, bp) > 0:
            info += 'However, the point is not on the segment AB.\n'
            flag = 1
        else:
            info += 'And, point is on the segment AB\n'
            flag = 2
            if np.array_equal(la, p):
                info += 'Point is on vertex A\n'
                flag = 3
            elif np.array_equal(lb, p):
                info += 'Point is on vertex B\n'
                flag = 3
    else:
        info = 'Point is not on line AB\n'
        flag = 4
    return flag, info


# Heron's formula is used to calculate the triangle area
def heron_formula(a, b, c):
    s = (a + b + c)/2
    return np.sqrt(s * (s - a) * (s - b) * (s - c))


def point_on_segment(la, lb, p):
    dist_to_line = dist(la, lb, p)

    ap = p - la
    bp = p - lb
    ab = lb - la

    cross = np.dot(ap, ab)
    d = np.linalg.norm(ab)
    if cross <= 0:
        return np.sqrt(cross)
    elif cross >= d:
        return np.linalg.norm(bp)
    else:
        return dist_to_line


def dist(la, lb, p): # distance from point p to line ab
    a = np.linalg.norm(p - la)
    b = np.linalg.norm(p - lb)
    c = np.linalg.norm(lb - la)
    area = heron_formula(a, b, c)
    return 2 * area / c

# Use Heron's formula to calculate the distance from a point to a line
def point_to_line(la, lb, p):
    dist_to_line = 0
    dist_to_seg_line = 0
    flag, info = point_on_line_check(la, lb, p)
    if not flag:
        info = 'Line is not available.'
        return dist_to_line, dist_to_seg_line, info
    else:
        dist_to_seg_line = point_on_segment(la, lb, p)
        if flag == 4:
            dist_to_line = dist(la, lb, p)
        else:
            dist_to_line = 0

    return dist_to_line, dist_to_seg_line, info


# Check a point is on right or left side of a line
# Only works on 2D space
def check_side(la, lb, p):
    ab = lb - la
    ap = p - la
    
    d = np.linalg.norm(np.cross(ab, ap)) # if d > 0, p is on the left side of ab; if d < 0, p is on the right side.
    
    if d > 0:
        return "Point is on the left side of line AB.\n"
    elif d < 0:
        return "Point is on the right side of line AB.\n"
    else:
        return "Point is on the line AB.\n"


def visualize2d(la, lb, p):
    arrow_size = 2
    text_size = 16
    plt.plot(p[0], p[1], 'ro')
    plt.plot(np.vstack((la, lb))[:, 0], np.vstack((la, lb))[:, 1], marker='o', zorder=3)
    plt.arrow(la[0], la[1], lb[0] - la[0], lb[1] - la[1], length_includes_head=True,
              head_width=arrow_size, head_length=arrow_size * 2, fc='b', ec='b', zorder=4)
    plt.text(la[0] + 1, la[1] + 3, 'A', fontsize= text_size, zorder=5)
    plt.text(lb[0] + 1, lb[1] + 3, 'B', fontsize= text_size, zorder=5)
    plt.text(p[0], p[1], 'P', fontsize= text_size, zorder=5)
    
    xmin = plt.axis()[0]
    xmax = plt.axis()[1]
    ymin = (xmin - la[0]) * (lb[1] - la[1]) / (lb[0] - la[0]) + la[1]
    ymax = (xmax - la[0]) * (lb[1] - la[1]) / (lb[0] - la[0]) + la[1]

    plt.plot([xmin, xmax], [ymin, ymax], '--')
    plt.show()


def visualize3d(la, lb, p):
    arrow_size = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.scatter(p[0], p[1], p[2], c='r', marker='^')
    #np.vstack: Stack arrays in sequence vertically
    ax.plot(np.vstack((la, lb))[:, 0], np.vstack((la, lb))[:, 1], np.vstack((la, lb))[:, 2], marker='o', zorder=3)
    ax.quiver(la[0], la[1], la[2], lb[0] - la[0], lb[1] - la[1], lb[2] - la[2])
    ax.text(la[0], la[1], la[2], 'A', fontsize=arrow_size * 2, zorder=5)
    ax.text(lb[0], lb[1], lb[2], 'B', fontsize=arrow_size * 2, zorder=5)
    ax.text(p[0], p[1], p[2], 'P', fontsize=arrow_size * 2, zorder=5)
    plt.show()


class Counter_program():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Point and Line")
        self.create_widgets()

        self.radio_variable = tk.StringVar()
        self.combobox_value = tk.StringVar()

    def create_widgets(self):
        self.window['padx'] = 15
        self.window['pady'] = 15

        entry_frame = ttk.LabelFrame(self.window, text="Data Entry",
                                     relief=tk.RIDGE)
        entry_frame.grid(row=2, column=4, sticky=tk.E + tk.W + tk.N + tk.S)

        output = ttk.LabelFrame(self.window, text="Output",
                                     relief=tk.RIDGE)
        output.grid(row=3, column=4, sticky=tk.E + tk.W + tk.N + tk.S)

        self.A = ttk.Label(entry_frame, text="A")
        self.A.grid(row=1, column=1, sticky=tk.W + tk.N)

        self.B = ttk.Label(entry_frame, text="B")
        self.B.grid(row=2, column=1, sticky=tk.W + tk.N)

        self.Ptest = ttk.Label(entry_frame, text="P")
        self.Ptest.grid(row=3, column=1, sticky=tk.W + tk.N)

        self.Out_msg = tk.Text(output, height=10, width=45)
        self.Out_msg.grid(row=1, column=1, sticky=tk.W, pady=3)
        self.Out_msg.insert(tk.END, "")

        self.Ax = ttk.Entry(entry_frame, width=12)
        self.Ax.grid(row=1, column=2, sticky=tk.W, pady=3)
        self.Ax.insert(tk.END, "56")

        self.Ay = ttk.Entry(entry_frame, width=12)
        self.Ay.grid(row=1, column=3, sticky=tk.W, pady=3)
        self.Ay.insert(tk.END, "77")

        self.Az = ttk.Entry(entry_frame, width=12)
        self.Az.grid(row=1, column=4, sticky=tk.W, pady=3)
        self.Az.insert(tk.END, "22")

        self.Bx = ttk.Entry(entry_frame, width=12)
        self.Bx.grid(row=2, column=2, sticky=tk.W, pady=3)
        self.Bx.insert(tk.END, "23")

        self.By = ttk.Entry(entry_frame, width=12)
        self.By.grid(row=2, column=3, sticky=tk.W, pady=3)
        self.By.insert(tk.END, "45")

        self.Bz = ttk.Entry(entry_frame, width=12)
        self.Bz.grid(row=2, column=4, sticky=tk.W, pady=3)
        self.Bz.insert(tk.END, "32")

        self.Ptestx = ttk.Entry(entry_frame, width=12)
        self.Ptestx.grid(row=3, column=2, sticky=tk.W, pady=3)
        self.Ptestx.insert(tk.END, "11")

        self.Ptesty = ttk.Entry(entry_frame, width=12)
        self.Ptesty.grid(row=3, column=3, sticky=tk.W, pady=3)
        self.Ptesty.insert(tk.END, "22")

        self.Ptestz = ttk.Entry(entry_frame, width=12)
        self.Ptestz.grid(row=3, column=4, sticky=tk.W, pady=3)
        self.Ptestz.insert(tk.END, "5")

        self.Calculate = ttk.Button(entry_frame, text="Process", command=self.process)
        self.Calculate.grid(row=4, column=1)

        self.Quit = ttk.Button(entry_frame, text="Quit", command=self.window.destroy)
        self.Quit.grid(row=4, column=2)

    def process(self):
        self.Out_msg.delete('1.0', tk.END)

        la = np.array([float(self.Ax.get()),
                       float(self.Ay.get()),
                       float(self.Az.get())])
        lb = np.array([float(self.Bx.get()),
                       float(self.By.get()),
                       float(self.Bz.get())])
        p = np.array([float(self.Ptestx.get()),
                      float(self.Ptesty.get()),
                      float(self.Ptestz.get())])
        if self.Az.get() == '0' and self.Bz.get() == '0' and self.Ptestz.get() == '0':
            flag = 1
        else:
            flag = 0

        out_info = ''
        dist_to_line, dist_to_seg_line, info = point_to_line(la, lb, p)
        out_info += info
        out_info += "The distance from point to line is: {}\n".format(dist_to_line)
        out_info += "The distance from point to segment line is: {}\n".format(dist_to_seg_line)
        out_info += check_side(la, lb, p)

        self.Out_msg.insert(tk.INSERT, out_info)

        if flag == 1:
            visualize2d(la, lb, p)
        else:
            visualize3d(la, lb, p)


if __name__ == "__main__":
    # Line AB, the direction is from A to B
    body = Counter_program()
    body.window.mainloop()
