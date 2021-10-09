from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name='shpaclass',
  packages = ['shpaclass'],
  version='0.1.0',
  author='Lovre',
  author_email='lovre.pesut@gmail.com',
  description='Classification algorithm based on finding shortest paths',
  long_description=long_description,
  url='https://github.com/rovle/shortest-path-classification',
  keywords=['machine learning', 'graphs'],
  license='MIT',
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  python_requires=">=3.6",
  install_requires=['networkx >= 2.5', 'numpy >= 1.19.2']
)
