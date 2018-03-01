"""
generate_README.py
~~~~~~~~~~~~~~~~~

This file automatically generates the README.md to include links to all the plots.

TODO:
    * make readme better
"""

import os

DEFAULT_README1 = '''
# Plots:
'''

plot_files = ["\n[{}](Plots/{})\n".format(f, f) for f in os.listdir('Plots/') if (f != '.DS_Store')]
plot_files_str = "\n".join(plot_files)

readme = DEFAULT_README1 + plot_files_str

f = open('README.md', 'w')
f.write(readme)
f.close()

