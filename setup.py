from distutils.core import setup

setup(
    name='PySky',
    version='0.1.3dev',
    author='Jon St. John',
    author_email='jonstjohn@gmail.com',
    packages=['pysky', 'pysky.test'],
    scripts=['bin/download','bin/forecast'],
    url='http://pypi.python.org/pypi/PySky/',
    license='LICENSE.txt',
    description='Weather toolkit',
    long_description=open('README.rst').read(),
    install_requires=[
        "python-dateutil >= 1.5",
    ],
)
