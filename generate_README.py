"""
generate_README.py
~~~~~~~~~~~~~~~~~

This file automatically generates a basic README.md to include links to all the plots.

"""

import os

DEFAULT_README1 = '''
# Plots:
'''
plots = os.listdir('Plots/')
plots.sort()

plot_files = list()

for plot in plots:
    if plot != '.DS_Store' and open('README.md', 'r').read().find(plot) < 0:
        plot_files.append("\n[{}](Plots/{})\n".format(plot, plot))

plot_files_str = "\n".join(plot_files)

readme = DEFAULT_README1 + plot_files_str

f = open('diff_README.md', 'w')
f.write(readme)
f.close()

