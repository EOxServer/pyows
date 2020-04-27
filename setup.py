# ------------------------------------------------------------------------------
#
# Project: pyows <http://github.com/geopython/pycql>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#
# ------------------------------------------------------------------------------
# Copyright (C) 2019 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

"""Install pyows."""

from setuptools import find_packages, setup
import os
import os.path

# don't install dependencies when building win readthedocs
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# get version number
# from https://github.com/mapbox/rasterio/blob/master/setup.py#L55
with open(os.path.join(os.path.dirname(__file__), 'ows/__init__.py')) as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break

# use README.md for project long_description
with open('README.md') as f:
    readme = f.read()


def parse_requirements(file):
    return sorted(set(
        line.partition('#')[0].strip()
        for line in open(os.path.join(os.path.dirname(__file__), file))
    ) - set(''))


install_requires = parse_requirements('requirements.txt') if not on_rtd else []

setup(
    name='pyows',
    version=version,
    description='OWS utilities',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Fabian Schindler',
    author_email='fabian.schindler@eox.at',
    url='https://github.com/eoxserver/pyows',
    license='MIT',
    packages=find_packages(),
    package_dir={'static': 'static'},
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=['pytest']
)
