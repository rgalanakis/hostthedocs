from setuptools import setup, find_packages

setup(
    name='hostthedocs',
    version='0.2.0',
    description='Makes documentation hosting easy.',
    author='Rob Galanakis',
    author_email='rob.galanakis@gmail.com',
    url='https://github.com/rgalanakis/hostthedocs',
    packages=find_packages(),
    install_requires=['Flask'],
)
