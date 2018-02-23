"""
generate_README.py
~~~~~~~~~~~~~~~~~

This file automatically generates the README.md to include links to all the plots.

TODO:
    * make readme better
"""

import os

DEFAULT_README1 = '''
# Project Title

This project scraps the data of coins of Augustus (Octavian) from the years 44BC to 14 AD from the British Museum website. In doing so, we can explore any relationships of the inscriptions, denomination, material, date, subjects, associated names and weight.

## Getting Started

Simply run the code in Analyze Data.ipynb to see the relationships

## Built With

* [Pandas](https://pandas.pydata.org) - Handling the "large" amounts of data
* And more...

## Authors

* **William Ma** - *Initial work* - [williamma12](https://github.com/williamma12)
* **Professor Diliana Angelova** - *Historical Expert* - [University of California, Berkeley History of Art faculty page](http://arthistory.berkeley.edu/person/1637809-diliana-angelova)

## License

This project is licensed under the GLP-3.0 License - see the [LICENSE.md](LICENSE.md) file for details

TODO:

 * Add Acknowledgements
 * Complete Built With list
 * Put location counts on map
     * Include interactivity with simulated time passage
 * Explore other relationships

## Plots:

'''

plot_files = ["[{}](Plots/{})".format(f, f) for f in os.listdir('Plots/') if (f != '.DS_Store')]
plot_files_str = "\n".join(plot_files)

readme = DEFAULT_README1 + plot_files_str

f = open('README.md', 'w')
f.write(readme)
f.close()

