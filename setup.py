import os
import re
from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(here, "pdoc", "__init__.py")) as f:
    VERSION = re.search(r'__version__ = "(.+?)"', f.read()).group(1)

setup(
    name="pdoc",
    author="Andrew Gallant",
    author_email="pdoc@burntsushi.net",
    version=VERSION,
    license="UNLICENSE",
    description="A simple program and library to auto generate API "
    "documentation for Python modules.",
    long_description=long_description,
    url="https://github.com/BurntSushi/pdoc",
    classifiers=[
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
        "License :: Public Domain",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    platforms="ANY",
    packages=["pdoc"],
    package_data={"pdoc/render": ["templates/*"]},
    entry_points={"console_scripts": ["pdoc = pdoc.cli:main"]},
    provides=["pdoc"],
    install_requires=[
        "mako>=1.0.7,<1.1",
        "markdown2>=2.3.5,<2.4",
        "pygments>=2.2.0,<2.3",
    ],
)
