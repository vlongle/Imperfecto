from setuptools import find_packages, setup

setup(
    name='imperfecto',
    version='1.0.0',
    author='Long Le',
    author_email='vietlong.lenguyen@gmail.com',
    description='Implementation of algorithms for imperfect information games in Python.',
    license='MIT',
    keywords='python imperfect info algorithms',
    url='https://github.com/vlongle/Imperfecto',
    packages=[pkg for pkg in find_packages() if pkg != "tests"],
    python_requires='>=3.10',
    install_requires=['click', 'numpy', 'enlighten'],
)
