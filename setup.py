import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system.
sys.path.pop(0)
from setuptools import setup


setup(
    name='micropython-microqueue',
    description='Simple redis queue for MicroPython',
    long_description="""MicroQueue is a Python module that allows you to use Redis as a message queue.
The resulting message queues are compatible with those provided by the python
hotqueue/redislite-hotqueue modules when used with the json serializer.  This code is written to work
properly in conjunction with the micropython-redis module to allow operation on resource constrained
embedded platforms.""",
    url='https://github.com/dhubbard/micropython-microqueue',
    author='Dwight Hubbard',
    author_email="dwight@dwighthubbard.com",
    install_requires=['micropython-redis.list'],
    license='MIT',
    maintainer='Dwight Hubbard',
    maintainer_email='dwight@dwighthubbard.com',
    packages=['microqueue'],
    version='0.0.4',
    zip_safe=True,
)
