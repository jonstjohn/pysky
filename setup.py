from distutils.core import setup

setup(
    name='PySky',
    version='0.1.0',
    author='Jon St. John',
    author_email='jonstjohn@gmail.com',
    packages=['pysky', 'pysky.test'],
    scripts=['bin/download','bin/forecast'],
    url='http://pypi.python.org/pypi/PySky/',
    license='LICENSE.txt',
    description='Weather toolkit',
    long_description=open('README.md').read(),
    install_requires=[
        "dateutil >= 1.5",
    ],
)
