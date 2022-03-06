from setuptools import setup, find_packages

setup(
    name='imperfect_info_games',
    version='1.0.0',
    author='Long Le',
    author_email='vietlong.lenguyen@gmail.com',
    description='Implementation of algorithms for imperfect information games in Python.',
    license='MIT',
    keywords='python imperfect info algorithms',
    url='https://github.com/vlongle/imperfect_information_games',
    packages=[pkg for pkg in find_packages() if pkg != "tests"],
)
