from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='awi_dws',
    python_requires='>= 3.6',
    version="0.1",
    description='Python wrapper for AWI Data Web Service',
    long_description=readme,
    author='Roland Koppe',
    license=license,
    py_modules=['dws'],
    install_requires=[  'pandas',
                        'requests',
                        ]
)
