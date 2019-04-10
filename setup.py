from setuptools import setup
import os

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)



# Probably should be changed, __init__.py is no longer required for Python 3
for dirpath, dirnames, filenames in os.walk('bonsai_api'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='bonsai_api',
    version="0.1dev",
    packages=packages,
    author="Romain Sacchi",
    author_email="r_s@me.com",
    license=open('LICENSE').read(),
    # Only if you have non-python data (CSV, etc.). Might need to change the directory name as well.
    # package_data={'your_name_here': package_files(os.path.join('bonsai_api', 'data'))},
    install_requires=[
        'appdirs',
        'docopt',
        'flask',
        'flask-restful',
        'sparqlwrapper'
    ],
    url="https://github.com/BONSAMURAIS/bonsai_api",
    long_description=open('README.md').read(),
    description='Romain Sacchi',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7',
    ],
)
