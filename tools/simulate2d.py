#!/usr/bin/env python3
# N-body GUI simulator

from tkinter import *

# Check parameters.
if len(sys.argv) < 2:
    print("Please specify arguments correctly.")
    print("Usage: simulate.py <result.txt> " +
          "[max_step [scale [center_x center_y [width height]]]]")
    sys.exit(0x1)

# Parameters
max_step = None if len(sys.argv) < 3 or \
                   float(sys.argv[2]) == -1 else float(sys.argv[2])
scale = 1 if len(sys.argv) < 4 else float(sys.argv[3])
center = None if len(sys.argv) < 6 else (float(sys.argv[4]),
                                         float(sys.argv[5]))
canvas_size = None if len(sys.argv) < 8 else (float(sys.argv[6]),
                                              float(sys.argv[7]))

# Basic 8 colors
'''
colors = ["red", "green", "blue", "magenta",
          "yellow", "cyan", "black", "white"]
'''
# Colors for Solar system except Neptune
colors = ["red", "black", "yellow", "blue",
          "magenta", "white", "green", "cyan"]

# Total coords of whole particles
total_coords = []

# The first draw flag
first_draw = True


# Open the result file.
def read_result_file(filename):
    with open(filename, "r") as f_in:
        global total_coords

        total_coords = []
        step_coords = []

        step = 1
        skip = True

        while True:
            if max_step is not None and step > max_step:
                break

            line = f_in.readline()
            if not line:
                total_coords.append(list(step_coords))
                break

            tokens = line.split()

            if tokens[0] == "n":
                if skip:
                    skip = False
                else:
                    total_coords.append(list(step_coords))
                    step_coords.clear()
                    step += 1
                continue

            if skip:
                continue

            step_coords.append((float(tokens[2]), float(tokens[3])))


# Canvas widget's resize event handler
def on_resize(event):
    global first_draw

    if center is not None and not first_draw:
        return

    first_draw = False
    event.widget.delete("all")

    for step_coords in total_coords:
        color_idx = 0

        for coords in step_coords:
            if center is None:
                x = event.width / 2 + coords[0] * scale
                y = event.height / 2 + coords[1] * -scale
            else:
                x = center[0] + coords[0] * scale
                y = center[1] + coords[1] * -scale

            event.widget.create_oval(x, y, x, y, outline=colors[color_idx])

            if len(colors) > 1:
                color_idx = color_idx + 1 if color_idx + 1 < len(colors) else 0


read_result_file(sys.argv[1])

top = Tk()
top.title("simulate2d")

if canvas_size is None:
    top.attributes("-zoomed", True)
    # top.attributes("-fullscreen", True)
    c = Canvas(top)
else:
    c = Canvas(top, width=canvas_size[0], height=canvas_size[1])

top.bind("<Escape>", lambda e: top.attributes("-fullscreen", False))
top.bind("<Key>", lambda e: top.attributes("-fullscreen", True)
         if e.char == "f" else None)

c.bind("<Configure>", on_resize)
c.pack(fill=BOTH, expand=YES)

top.mainloop()
