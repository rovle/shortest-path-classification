from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name='shapaclass',
  packages = ['shapaclass'],
  version='0.1.2',
  author='Lovre',
  author_email='lovre.pesut@gmail.com',
  description='Classification algorithm based on finding shortest paths',
  long_description=long_description,
  long_description_content_type='text/markdown',
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
