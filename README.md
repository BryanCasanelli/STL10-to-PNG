# STL10-to-PNG
Python script to transform the binary STL-10 dataset (http://cs.stanford.edu/~acoates/stl10/) into PNG image files.

    Usage: python/python3 stl10_to_png.py [OPTIONS]

      OPTIONS:
      -h  --help      : Show this help.
      -d  --download  : Download the dataset and extract it.
                        If the file is already downloaded, then only extract it.

Warning: Transform the unlabeled data into images requires approximately 3 GB of free RAM.

Developed by Bryan Casanelli based on STL10 by Martin Tutek (https://github.com/mttk/STL10).
