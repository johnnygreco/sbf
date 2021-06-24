import os, sys
import builtins
from setuptools import setup, find_packages
sys.path.append('src')


def readme():
    with open("README.rst") as f:
        return f.read()


# HACK: fetch version
builtins.__SBF_SETUP__ = True
import sbf
version = sbf.__version__


# Publish the library to PyPI.
if "publish" in sys.argv[-1]:
    os.system("python setup.py sdist bdist_wheel")
    os.system(f"python3 -m twine upload dist/*{version}*")
    sys.exit()


# Push a new tag to GitHub.
if "tag" in sys.argv:
    os.system("git tag -a {0} -m 'version {0}'".format(version))
    os.system("git push --tags")
    sys.exit()


setup(
    name='sbf',
    version=version,
    description='SBF made simple.',
    long_description=readme(),
    author='Johnny Greco',
    author_email='jgreco.astro@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    url='https://github.com/johnnygreco/',
    install_requires=[
        'numpy>=1.17',
        'scipy>=1',
        'matplotlib>=3',
        'sep=>1'
     ],
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Astronomy",
      ],
    python_requires='>=3.6',
)
