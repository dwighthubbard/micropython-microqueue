import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup


setup(
    name='micropython-microqueue',
    description='Simple redis queue for MicroPython',
    long_description="""This is a simple redis queue for micropython.""",
    url='https://github.com/dhubbard/micropython-redis',
    author='Dwight Hubbard',
    author_email="dwight@dwighthubbard.com",
    install_requires=['micropython-redis.list'],
    license='MIT',
    maintainer='Dwight Hubbard',
    maintainer_email='dwight@dwighthubbard.com',
    packages=['microqueue'],
    version='0.0.2',
    zip_safe=True,
)
