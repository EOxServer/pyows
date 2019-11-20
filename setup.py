
import os
from setuptools import setup

# TODO: read READMe.rst and assign it to 'long_description'
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


packages, data_files = [], []
for dirpath, dirnames, filenames in os.walk('ows'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append(
            [dirpath, [os.path.join(dirpath, f) for f in filenames]]
        )


# On readthecods.org we don't want the reftools to be build
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    ext_modules = []

setup(
    name='pyows',
    version='0.0.1',
    packages=packages,
    data_files=data_files,
    include_package_data=True,
    scripts=[
    ],
    install_requires=[
        ],
    zip_safe=False,

    # Metadata
    author="EOX IT Services GmbH",
    author_email="office@eox.at",
    maintainer="EOX IT Services GmbH",
    maintainer_email="packages@eox.at",

    description="OWS request/response encoding/decoding",
    long_description="",

    classifiers=[
        'Development Status :: 0 - Production',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
    ],

    license="EOxServer Open License (MIT-style)",
    keywords="Earth Observation, EO, OGC, WCS, WMS",
    url="http://eoxserver.org/"
)
