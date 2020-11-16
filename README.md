# Prof Stick's Mostly Good Python Project Template

A template which provides the structure for Python 3 projects enabling:
* creation of modules
* Google type docstrings for classes, methods and functions
* version control in Github
* automatic generation of documents using sphinx
* publishing to read the docs

## Motivation
'We hold this truth to be self-evident,' a well planned and documented project in a good thing in too many ways to enumerate. However, many beginners, especially students, often see document and structure as things which get in the way of project development rather than being intrinsic to it. This template hopes to encourage good habits by making it as easy as possible to write well documented code with an appropriate file structure that follows conventions and allows version control and automatic generation and publishing of documents. The hope is that when students see how much can be achieved with a little bit of extra effort, and experience the joy of publishing their projects with documentation, they will develop good lifelong habits.

## File Structure
This template has the following file structure based on the structure recommended by [Kenneth Reitz, Repository Structure and Python](https://kenreitz.org/essays/repository-structure-and-python)

```text
package_name
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── docs
│ ├── build
│ ├── make.bat
│ ├── Makefile
│ └── source
├── module1
│ └── module1.py
├── module2_name
│ └── module2.py
└── tests
  ├── test_module1.py
  └── test_module2.py
```

## Resources
For more information consult:
* [Python 3 latest version documentation](https://docs.python.org/3/)
* [Mastering Markdown](https://guides.github.com/features/mastering-markdown/)
* [Restructured Text (reST) and Sphinx CheatSheet](https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html)
* [A “How to” Guide for Sphinx + ReadTheDocs](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/index.html)
* [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html)
* [Structuring Your Project](https://docs.python-guide.org/writing/structure/)
* [Repository Structure and Python](https://kenreitz.org/essays/repository-structure-and-python)
* [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code)


## NOTES
ATM is seems like there is no way to use a relative reference to the root `README.md` for building the sphinx documentation in Windows. To solve this the conf.py file includes some script for copying the `README.md` file from the root to the `/docs/source/` directory overwriting any README file that is there. So only edit the README in the root directory. This behaviour can be commented out if undesired.

### TODO

Implement the following recommendations from [Repository Structure and Python](https://kenreitz.org/essays/repository-structure-and-python)

```text
Obviously, these test modules must import your packaged module to test it. You can do this a few ways:

    Expect the package to be installed in site-packages.
    Use a simple (but explicit) path modification to resolve the package properly.

I highly recommend the latter. Requiring a developer to run setup.py develop to test an actively changing codebase also requires them to have an isolated environment setup for each instance of the codebase.

To give the individual tests import context, create a tests/context.py file:

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import sample

Then, within the individual test modules, import the module like so:

from .context import sample```
