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

plot_files = ["\n[{}](Plots/{})\n".format(f, f) for f in plots if (f != '.DS_Store')]
plot_files_str = "\n".join(plot_files)

readme = DEFAULT_README1 + plot_files_str

f = open('basic_README.md', 'w')
f.write(readme)
f.close()

