from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Viridis

output_file("line.html")

p = figure(plot_width=400, plot_height=400)

lines = [([1, 2, 3, 4, 5], [6, 7, 2, 4, 5]), ([2, 3, 4, 5, 6], [6, 7, 2, 4, 5]), ([2, 3, 4, 5, 6], [5, 2, 4, 2, 1]),
         ([1, 2, 3, 4, 5], [5, 2, 4, 1, 2]), ([1, 2, 3, 4, 5], [9, 2, 3, 6, 4])]
# add a line renderer
for line, color in zip(lines, Viridis[len(lines)]):
    p.line(*line, line_width=2, color=color)

show(p)